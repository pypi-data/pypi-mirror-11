__author__ = 'Bohdan Mushkevych'

from datetime import datetime
from logging import INFO, WARNING, ERROR

from synergy.db.model import job
from synergy.db.model.job import Job
from synergy.db.error import DuplicateKeyError
from synergy.db.dao.unit_of_work_dao import UnitOfWorkDao
from synergy.db.dao.job_dao import JobDao
from synergy.db.model import unit_of_work
from synergy.db.model.unit_of_work import UnitOfWork
from synergy.db.model.synergy_mq_transmission import SynergyMqTransmission
from synergy.mq.flopsy import PublishersPool
from synergy.conf import context
from synergy.system.decorator import with_reconnect
from synergy.scheduler.tree_node import NodesCompositeState
from synergy.scheduler.scheduler_constants import TYPE_MANAGED


class AbstractStateMachine(object):
    """ Abstract state machine used to govern all processes and their states """

    def __init__(self, logger, timetable, name):
        self.name = name
        self.logger = logger
        self.publishers = PublishersPool(self.logger)
        self.timetable = timetable
        self.uow_dao = UnitOfWorkDao(self.logger)
        self.job_dao = JobDao(self.logger)

    def __del__(self):
        try:
            self.logger.info('Closing Flopsy Publishers Pool...')
            self.publishers.close()
        except Exception as e:
            self.logger.error('Exception caught while closing Flopsy Publishers Pool: %s' % str(e))

    def _log_message(self, level, process_name, timeperiod, msg):
        """ method performs logging into log file and Timetable's tree node"""
        self.timetable.add_log_entry(process_name, timeperiod, msg)
        self.logger.log(level, msg)

    @with_reconnect
    def _insert_uow(self, process_name, start_timeperiod, end_timeperiod, start_id, end_id):
        """creates unit_of_work and inserts it into the DB
            :raise DuplicateKeyError: if unit_of_work with given parameters already exists """
        uow = UnitOfWork()
        uow.process_name = process_name
        uow.timeperiod = start_timeperiod
        uow.start_id = str(start_id)
        uow.end_id = str(end_id)
        uow.start_timeperiod = start_timeperiod
        uow.end_timeperiod = end_timeperiod
        uow.created_at = datetime.utcnow()
        uow.source = context.process_context[process_name].source
        uow.sink = context.process_context[process_name].sink
        uow.state = unit_of_work.STATE_REQUESTED
        uow.unit_of_work_type = TYPE_MANAGED
        uow.number_of_retries = 0
        uow.arguments = context.process_context[process_name].arguments
        uow.db_id = self.uow_dao.insert(uow)

        msg = 'Created: UOW %s for %s in timeperiod %s.' \
              % (uow.db_id, process_name, start_timeperiod)
        self._log_message(INFO, process_name, start_timeperiod, msg)
        return uow

    def _publish_uow(self, uow):
        mq_request = SynergyMqTransmission(process_name=uow.process_name, unit_of_work_id=uow.db_id)

        publisher = self.publishers.get(uow.process_name)
        publisher.publish(mq_request.document)
        publisher.release()

        msg = 'Published: UOW %r for %r in timeperiod %r.' % (uow.db_id, uow.process_name, uow.start_timeperiod)
        self._log_message(INFO, uow.process_name, uow.start_timeperiod, msg)

    def insert_and_publish_uow(self, process_name, start_timeperiod, end_timeperiod, start_id, end_id):
        """ method creates and publishes a unit_of_work. it also handles DuplicateKeyError and attempts recovery
        :return: tuple (uow, is_duplicate)
        :raise UserWarning: if the recovery from DuplicateKeyError was unsuccessful
        """
        is_duplicate = False
        try:
            uow = self._insert_uow(process_name, start_timeperiod, end_timeperiod, start_id, end_id)
        except DuplicateKeyError as e:
            is_duplicate = True
            msg = 'Catching up with latest unit_of_work %s in timeperiod %s, because of: %r' \
                  % (process_name, start_timeperiod, e)
            self._log_message(WARNING, process_name, start_timeperiod, msg)
            uow = self.uow_dao.recover_from_duplicatekeyerror(e)

        if uow is None:
            msg = 'MANUAL INTERVENTION REQUIRED! Unable to locate unit_of_work for %s in %s' \
                  % (process_name, start_timeperiod)
            self._log_message(WARNING, process_name, start_timeperiod, msg)
            raise UserWarning(msg)

        # publish the created/caught up unit_of_work
        self._publish_uow(uow)
        return uow, is_duplicate

    def shallow_state_update(self, uow):
        """ method does not trigger any new actions
        if applicable, it will update job_record state and Timetable tree node state
        :assumptions: uow is in [STATE_NOOP, STATE_CANCELED, STATE_PROCESSED] """
        pass

    def _is_noop_timeperiod(self, process_name, timeperiod):
        """ method verifies if the given timeperiod for given process is valid or falls in-between grouping checkpoints
        :param process_name: name of the process
        :param timeperiod: timeperiod to verify
        :return: False, if given process has no time_grouping set or it is equal to 1. False if time_grouping is custom
        but the given timeperiod matches the grouped timeperiod. True if the timeperiod falls in-between grouping cracks
        """
        time_grouping = context.process_context[process_name].time_grouping
        if time_grouping == 1:
            return False

        process_hierarchy = self.timetable.get_tree(process_name).process_hierarchy
        timeperiod_dict = process_hierarchy[process_name].timeperiod_dict
        return timeperiod_dict._translate_timeperiod(timeperiod) != timeperiod

    def _process_noop_timeperiod(self, job_record):
        """ method is valid for processes having time_grouping != 1.
            should a job record fall in-between grouped time milestones,
            its state should be set to STATE_NOOP without any processing """
        job_record.state = job.STATE_NOOP
        self.job_dao.update(job_record)
        tree = self.timetable.get_tree(job_record.process_name)
        tree.update_node(job_record)

        time_grouping = context.process_context[job_record.process_name].time_grouping
        msg = '%s job for timeperiod %r with time_grouping %r was transferred the job to STATE_NOOP' \
              % (job_record.process_name, job_record.timeperiod, time_grouping)
        self._log_message(INFO, job_record.process_name, job_record.timeperiod, msg)

    def _process_state_embryo(self, job_record):
        """ method that takes care of processing job records in STATE_EMBRYO state"""
        pass

    def _process_state_in_progress(self, job_record):
        """ method that takes care of processing job records in STATE_IN_PROGRESS state"""
        pass

    def _process_state_final_run(self, job_record):
        """method takes care of processing job records in STATE_FINAL_RUN state"""
        uow = self.uow_dao.get_one(job_record.related_unit_of_work)
        if uow.is_processed:
            self.timetable.update_job_record(job_record, uow, job.STATE_PROCESSED)
        elif uow.is_noop:
            self.timetable.update_job_record(job_record, uow, job.STATE_NOOP)
        elif uow.is_canceled:
            self.timetable.update_job_record(job_record, uow, job.STATE_SKIPPED)
        elif uow.is_invalid:
            msg = 'Job record %s: UOW for %s in timeperiod %s is in %s; ' \
                  'relying on the Garbage Collector to transfer UOW into the %s' \
                  % (job_record.db_id, job_record.process_name, job_record.timeperiod,
                     uow.state, unit_of_work.STATE_CANCELED)
            self._log_message(INFO, job_record.process_name, job_record.timeperiod, msg)
        else:
            msg = 'Suppressed creating uow for %s in timeperiod %s; job record is in %s; uow is in %s' \
                  % (job_record.process_name, job_record.timeperiod, job_record.state, uow.state)
            self._log_message(INFO, job_record.process_name, job_record.timeperiod, msg)

        timetable_tree = self.timetable.get_tree(job_record.process_name)
        timetable_tree.build_tree()

    def _process_terminal_state(self, job_record):
        """ method logs a warning message notifying that the job is no longer govern by this state machine """
        msg = 'Job record %s for %s at %s is in the terminal state %s, ' \
              'and is no further govern by the State Machine %s' \
              % (job_record.db_id, job_record.process_name, job_record.timeperiod, job_record.state, self.name)
        self._log_message(WARNING, job_record.process_name, job_record.timeperiod, msg)

    def manage_job_with_blocking_children(self, job_record, run_on_active_timeperiod):
        """ method will trigger job processing only if all children are in STATE_PROCESSED or STATE_SKIPPED
         and if all external dependencies are finalized (i.e. in STATE_PROCESSED or STATE_SKIPPED) """
        is_job_finalizable = self.timetable.is_job_record_finalizable(job_record)
        composite_state = self.timetable.dependent_on_composite_state(job_record)

        if is_job_finalizable:
            self.manage_job(job_record)
        elif composite_state.all_healthy and run_on_active_timeperiod:
            self.manage_job(job_record)
        else:
            msg = '%s for timeperiod %r is blocked by unprocessed children/dependencies. Waiting another tick' \
                  % (job_record.process_name, job_record.timeperiod)
            self._log_message(INFO, job_record.process_name, job_record.timeperiod, msg)

    def manage_job_with_blocking_dependencies(self, job_record, run_on_active_timeperiod):
        """ method will trigger job processing only if _all_ dependencies are in STATE_PROCESSED
         method will transfer current job into STATE_SKIPPED if any dependency is in STATE_SKIPPED """
        composite_state = self.timetable.dependent_on_composite_state(job_record)
        assert isinstance(composite_state, NodesCompositeState)

        if composite_state.all_processed:
            self.manage_job(job_record)
        elif composite_state.all_healthy and run_on_active_timeperiod:
            self.manage_job(job_record)
        elif composite_state.skipped_present:
            # As soon as among <dependent on> periods are in STATE_SKIPPED
            # there is very little sense in waiting for them to become STATE_PROCESSED
            # Skip this timeperiod itself
            job_record.state = job.STATE_SKIPPED
            self.job_dao.update(job_record)
            tree = self.timetable.get_tree(job_record.process_name)
            tree.update_node(job_record)

            msg = '%s for timeperiod %r is blocked by STATE_SKIPPED dependencies. ' \
                  'Transferred the job to STATE_SKIPPED' % (job_record.process_name, job_record.timeperiod)
            self._log_message(WARNING, job_record.process_name, job_record.timeperiod, msg)
        else:
            msg = '%s for timeperiod %r is blocked by unprocessed dependencies. Waiting another tick' \
                  % (job_record.process_name, job_record.timeperiod)
            self._log_message(INFO, job_record.process_name, job_record.timeperiod, msg)

    def manage_job(self, job_record):
        """ method main duty - is to _avoid_ publishing another unit_of_work, if previous was not yet processed
        In case the Scheduler sees that the unit_of_work is pending it could either update boundaries of the processing
        or wait another tick """
        assert isinstance(job_record, Job)

        if self._is_noop_timeperiod(job_record.process_name, job_record.timeperiod):
            self._process_noop_timeperiod(job_record)
            return

        try:
            if job_record.is_embryo:
                self._process_state_embryo(job_record)

            elif job_record.is_in_progress:
                self._process_state_in_progress(job_record)

            elif job_record.is_final_run:
                self._process_state_final_run(job_record)

            elif job_record.is_skipped:
                self._process_terminal_state(job_record)

            elif job_record.is_processed:
                self._process_terminal_state(job_record)

            elif job_record.is_noop:
                self._process_terminal_state(job_record)

            else:
                msg = 'Unknown state %s of the job %s' % (job_record.state, job_record.db_id)
                self._log_message(ERROR, job_record.process_name, job_record.timeperiod, msg)

        except LookupError as e:
            self.timetable.failed_on_processing_job_record(job_record.process_name, job_record.timeperiod)
            msg = 'Increasing fail counter for %s in timeperiod %s, because of: %r' \
                  % (job_record.process_name, job_record.timeperiod, e)
            self._log_message(WARNING, job_record.process_name, job_record.timeperiod, msg)
