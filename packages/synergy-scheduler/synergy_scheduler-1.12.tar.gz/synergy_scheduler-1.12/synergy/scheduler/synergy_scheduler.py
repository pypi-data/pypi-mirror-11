__author__ = 'Bohdan Mushkevych'

from datetime import datetime, timedelta
from threading import Lock

from amqp import AMQPError

from synergy.conf import context
from synergy.mq.flopsy import PublishersPool
from synergy.mx.synergy_mx import MX
from synergy.db.manager import db_manager
from synergy.db.model.managed_process_entry import ManagedProcessEntry
from synergy.db.model.freerun_process_entry import FreerunProcessEntry
from synergy.db.dao.freerun_process_dao import FreerunProcessDao
from synergy.system import time_helper
from synergy.system.decorator import with_reconnect, thread_safe
from synergy.system.synergy_process import SynergyProcess
from synergy.scheduler.garbage_collector import GarbageCollector
from synergy.scheduler.status_bus_listener import StatusBusListener
from synergy.scheduler.scheduler_constants import *
from synergy.scheduler.timetable import Timetable
from synergy.scheduler.thread_handler import ThreadHandlerHeader, ManagedThreadHandler, FreerunThreadHandler


class Scheduler(SynergyProcess):
    """ Scheduler hosts:
        - timetable: container for job tress and state machines
        - GarbageCollector: recycles failed/stalled unit of works
        - freerun and managed thread handlers: logic to trigger job execution
        - StatusBarListener: MQ Listener of workers feedback
        - MX: HTTP server with management UI """

    def __init__(self, process_name):
        super(Scheduler, self).__init__(process_name)
        self.lock = Lock()
        self.logger.info('Starting %s' % self.process_name)
        self.publishers = PublishersPool(self.logger)
        self.managed_handlers = dict()
        self.freerun_handlers = dict()
        self.timetable = Timetable(self.logger)
        self.freerun_process_dao = FreerunProcessDao(self.logger)

        self.gc = GarbageCollector(self)
        self.bus_listener = StatusBusListener(self)
        self.mx = MX(self)
        self.logger.info('Started %s' % self.process_name)

    def __del__(self):
        self.mx.stop()
        self.bus_listener.stop()
        self.gc.stop()

        for key, handler in self.managed_handlers.items():
            handler.deactivate(update_persistent=False)
        self.managed_handlers.clear()

        for key, handler in self.freerun_handlers.items():
            handler.deactivate(update_persistent=False)
        self.freerun_handlers.clear()

        self.publishers.close()

        super(Scheduler, self).__del__()

    def _register_process_entry(self, process_entry, call_back):
        """ method parses process_entry and creates a timer_handler out of it
         timer_handler is enlisted to either :self.freerun_handlers or :self.managed_handlers
         timer_handler is started, unless it is marked as STATE_OFF """
        trigger_frequency = process_entry.trigger_frequency
        if isinstance(process_entry, ManagedProcessEntry):
            handler_key = process_entry.process_name
            handler = ManagedThreadHandler(self.logger, handler_key, trigger_frequency, call_back, process_entry)
            self.managed_handlers[handler.key] = handler
        elif isinstance(process_entry, FreerunProcessEntry):
            handler_key = (process_entry.process_name, process_entry.entry_name)
            handler = FreerunThreadHandler(self.logger, handler_key, trigger_frequency, call_back, process_entry)
            self.freerun_handlers[handler.key] = handler
        else:
            raise ValueError('ProcessEntry type {0} is not known to the system. Skipping it.'
                             .format(process_entry.__class__.__name__))

        if process_entry.is_on:
            handler.activate()
            self.logger.info('Started scheduler thread for %s:%r.'
                             % (handler.handler_type, handler.key))
        else:
            self.logger.info('Handler for %s:%r registered in Scheduler. Idle until activated.'
                             % (handler.handler_type, handler.key))

    # **************** Scheduler Methods ************************
    def _load_managed_entries(self):
        """ loads scheduler managed entries. no start-up procedures are performed """
        for process_name, process_entry in context.process_context.items():
            if process_entry.process_type == TYPE_MANAGED:
                function = self.fire_managed_worker
            elif process_entry.process_type in [TYPE_FREERUN, TYPE_DAEMON]:
                self.logger.info('%s of type %s is found in context, but not managed by Synergy Scheduler. '
                                 'Skipping the process.'
                                 % (process_name, process_entry.process_type.upper()))
                continue
            else:
                self.logger.error('Type %s of process %s is not known to the system. Skipping it.' %
                                  (process_entry.process_type, process_name))
                continue

            try:
                self._register_process_entry(process_entry, function)
            except Exception:
                self.logger.error('Scheduler Handler %r failed to start. Skipping it.' % (process_entry.key,),
                                  exc_info=True)

    def _load_freerun_entries(self):
        """ reads scheduler managed entries and starts their timers to trigger events """
        freerun_entries = self.freerun_process_dao.get_all()
        for freerun_entry in freerun_entries:
            try:
                self._register_process_entry(freerun_entry, self.fire_freerun_worker)
            except Exception:
                self.logger.error('Scheduler Handler %r failed to start. Skipping it.' % (freerun_entry.key,),
                                  exc_info=True)

    @with_reconnect
    def start(self, *_):
        """ reads managed process entries and starts timer instances; starts dependant threads """
        db_manager.synch_db()
        self._load_managed_entries()

        try:
            self._load_freerun_entries()
        except LookupError as e:
            self.logger.warn('DB Lookup: %s' % str(e))

        # Scheduler is initialized and running. GarbageCollector can be safely started
        self.gc.start()

        # Scheduler is initialized and running. Status Bus Listener can be safely started
        self.bus_listener.start()

        # Scheduler is initialized and running. Management Extension (MX) can be safely started
        self.mx.start()

    @thread_safe
    def fire_managed_worker(self, thread_handler_header):
        """requests next valid job for given process and manages its state"""

        def _fire_worker(process_entry, prev_job_record):
            assert isinstance(process_entry, ManagedProcessEntry)
            job_record = self.timetable.get_next_job_record(process_entry.process_name)
            state_machine = self.timetable.state_machines[process_entry.state_machine_name]
            if job_record == prev_job_record:
                # avoid the loop
                return None

            run_on_active_timeperiod = process_entry.run_on_active_timeperiod
            if not run_on_active_timeperiod:
                time_qualifier = process_entry.time_qualifier
                incremented_timeperiod = time_helper.increment_timeperiod(time_qualifier, job_record.timeperiod)
                dt_record_timestamp = time_helper.synergy_to_datetime(time_qualifier, incremented_timeperiod)
                dt_record_timestamp += timedelta(minutes=LAG_5_MINUTES)

                if datetime.utcnow() <= dt_record_timestamp:
                    self.logger.info('Job record %s for timeperiod %s will not be triggered until %s.'
                                     % (job_record.db_id,
                                        job_record.timeperiod,
                                        dt_record_timestamp.strftime('%Y-%m-%d %H:%M:%S')))
                    return None

            blocking_type = process_entry.blocking_type
            if blocking_type == BLOCKING_DEPENDENCIES:
                state_machine.manage_job_with_blocking_dependencies(job_record, run_on_active_timeperiod)
            elif blocking_type == BLOCKING_CHILDREN:
                state_machine.manage_job_with_blocking_children(job_record, run_on_active_timeperiod)
            elif blocking_type == BLOCKING_NORMAL:
                state_machine.manage_job(job_record)
            else:
                raise ValueError('Unknown managed process type %s' % blocking_type)

            return job_record

        try:
            assert isinstance(thread_handler_header, ThreadHandlerHeader)
            self.logger.info('%r {' % (thread_handler_header.key, ))

            job_record = _fire_worker(thread_handler_header.process_entry, None)
            while job_record and job_record.is_finished:
                job_record = _fire_worker(thread_handler_header.process_entry, job_record)

        except (AMQPError, IOError) as e:
            self.logger.error('AMQPError: %s' % str(e), exc_info=True)
            self.publishers.reset_all(suppress_logging=True)
        except Exception as e:
            self.logger.error('Exception: %s' % str(e), exc_info=True)
        finally:
            self.logger.info('}')

    @thread_safe
    def fire_freerun_worker(self, thread_handler_header):
        """fires free-run worker with no dependencies to track"""
        try:
            assert isinstance(thread_handler_header, ThreadHandlerHeader)
            self.logger.info('%r {' % (thread_handler_header.key, ))

            state_machine = self.timetable.state_machines[STATE_MACHINE_FREERUN]
            state_machine.manage_schedulable(thread_handler_header.process_entry)

        except Exception as e:
            self.logger.error('fire_freerun_worker: %s' % str(e))
        finally:
            self.logger.info('}')


if __name__ == '__main__':
    from synergy.scheduler.scheduler_constants import PROCESS_SCHEDULER

    source = Scheduler(PROCESS_SCHEDULER)
    source.start()
