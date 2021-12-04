from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from avaliacao.views import strike_routine, rewards_routine


def start_strike():
    scheduler = BackgroundScheduler()
    scheduler.add_job(strike_routine, 'cron', day_of_week='tue-sun', hour=2, minute=50)
    scheduler.start()


def start_rewards():
    scheduler = BackgroundScheduler()
    # Schedule marcado para 23:50(02:50 UTC) da noite de Sabado(Domingo UTC)
    scheduler.add_job(rewards_routine, 'cron', day_of_week='sun', hour=2, minute=50)
    scheduler.start()
