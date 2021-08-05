from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from avaliacao.views import weekRoutine, rewardsRoutine


def start_week():
    scheduler = BackgroundScheduler()
    scheduler.add_job(weekRoutine, 'cron', day_of_week='tue-sun', hour=2, minute=50)
    scheduler.start()


def start_rewards():
    scheduler = BackgroundScheduler()
    scheduler.add_job(rewardsRoutine, 'cron', day_of_week='sun', hour=2, minute=50)
    scheduler.start()
