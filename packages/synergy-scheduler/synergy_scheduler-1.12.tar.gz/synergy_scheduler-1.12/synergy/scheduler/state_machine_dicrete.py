__author__ = 'Bohdan Mushkevych'

from logging import ERROR

from synergy.db.model import job
from synergy.scheduler.scheduler_constants import STATE_MACHINE_DISCRETE
from synergy.scheduler.abstract_state_machine import AbstractStateMachine
from synergy.system import time_helper
from synergy.conf import context


class StateMachineDiscrete(AbstractStateMachine):
    """ State Machine to handle discrete timeperiod boundaries for batch jobs
        in comparison to StateMachineContinuous this one does not re-compute processing boundaries"""

    def __init__(self, logger, timetable, name=STATE_MACHINE_DISCRETE):
        super(StateMachineDiscrete, self).__init__(logger, timetable, name)

    def __del__(self):
        super(StateMachineDiscrete, self).__del__()

    def notify(self, uow):
        tree = self.timetable.get_tree(uow.process_name)
        node = tree.get_node(uow.process_name, uow.timeperiod)
        job_record = node.job_record

        if not job_record.is_final_run:
            self.logger.info('Suppressing job state change since the job for {0} in {1} is not in STATE_FINAL_RUN'
                             .format(uow.process_name, uow.timeperiod))
            return
        self._process_state_final_run(job_record)

    def _process_state_embryo(self, job_record):
        """ method that takes care of processing job records in STATE_EMBRYO state"""
        time_qualifier = context.process_context[job_record.process_name].time_qualifier
        end_timeperiod = time_helper.increment_timeperiod(time_qualifier, job_record.timeperiod)
        uow, is_duplicate = self.insert_and_publish_uow(job_record.process_name,
                                                        job_record.timeperiod,
                                                        end_timeperiod,
                                                        0,
                                                        0)
        self.update_job(job_record, uow, job.STATE_IN_PROGRESS)

    def _process_state_in_progress(self, job_record):
        """ method that takes care of processing job records in STATE_IN_PROGRESS state"""
        def _process_state(target_state, uow):
            if uow.is_active:
                # Large Job processing takes more than 1 tick of the Scheduler
                # Let the Job processing complete - do no updates to Scheduler records
                pass
            elif uow.is_finished:
                # create new uow to cover new inserts
                new_uow, is_duplicate = self.insert_and_publish_uow(job_record.process_name,
                                                                    job_record.timeperiod,
                                                                    end_timeperiod,
                                                                    0,
                                                                    int(uow.end_id) + 1)
                self.update_job(job_record, new_uow, target_state)

        time_qualifier = context.process_context[job_record.process_name].time_qualifier
        end_timeperiod = time_helper.increment_timeperiod(time_qualifier, job_record.timeperiod)
        actual_timeperiod = time_helper.actual_timeperiod(time_qualifier)
        is_job_finalizable = self.timetable.is_job_record_finalizable(job_record)
        uow = self.uow_dao.get_one(job_record.related_unit_of_work)

        if job_record.timeperiod == actual_timeperiod or is_job_finalizable is False:
            _process_state(job.STATE_IN_PROGRESS, uow)

        elif job_record.timeperiod < actual_timeperiod and is_job_finalizable is True:
            _process_state(job.STATE_FINAL_RUN, uow)

        else:
            msg = 'Job record {0} has timeperiod from future {1} vs current time {2}' \
                  .format(job_record.db_id, job_record.timeperiod, actual_timeperiod)
            self._log_message(ERROR, job_record.process_name, job_record.timeperiod, msg)
