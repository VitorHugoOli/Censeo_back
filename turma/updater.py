from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from turma.views import checkTimeForOpenClass


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(checkTimeForOpenClass, 'interval', minutes=1)
    scheduler.start()