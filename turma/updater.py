from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from turma.views import check_time_for_open_class


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_time_for_open_class, 'interval', minutes=1)
    scheduler.start()