from django_cron import CronJobBase, Schedule

from main import functions


class UpdateData(CronJobBase):
    RUN_AT_TIMES = ['2:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'main.update_data'

    def do(self):
    	functions.update()
