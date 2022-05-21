import logging
import time
from datetime import datetime

from django.conf import settings
from sheets.models import Order

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from apscheduler.schedulers.background import BackgroundScheduler

import telegram_send
import requests
import gspread
import pandas as pd
import telegram_send
import xml.etree.ElementTree as ET
import requests
from sheets.creds import credentials


scheduler = BackgroundScheduler({'apscheduler.daemon': False})

logger = logging.getLogger(__name__)


def validate_delivery():
    records = Order.objects.all()
    today = datetime.today()
    today_str = today.strftime("%Y-%m-%d")
    today_date = datetime.strptime(today_str, "%Y-%m-%d")
    for record in records:
        if record.delivery_time < today_date.date():
            telegram_send.send(
                messages=[
                  f"{record.number} поставка {record.delivery_time} просроченна"
                ]
            )


def sheet_update():
    r = requests.post("http://0.0.0.0:5000/service/sheet/")
    logger.info(f"Google sheet update at {datetime.now()}")
    return r.status_code


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # scheduler.add_job(
    #   my_job,
    #   trigger=CronTrigger(second="*/10"),  # Every 10 seconds
    #   id="my_job",  # The `id` assigned to each job MUST be unique
    #   max_instances=1,
    #   replace_existing=True,
    # )
    # logger.info("Added job 'my_job'.")

    scheduler.add_job(
      delete_old_job_executions,
      trigger=CronTrigger(
        day_of_week="mon", hour="00", minute="00"
      ),  # Midnight on Monday, before start of the next work week.
      id="delete_old_job_executions",
      max_instances=1,
      replace_existing=True,
    )
    logger.info(
      "Added weekly job: 'delete_old_job_executions'."
    )

    try:
      logger.info("Starting scheduler...")
      scheduler.start()
    except KeyboardInterrupt:
      logger.info("Stopping scheduler...")
      scheduler.shutdown()
      logger.info("Scheduler shut down successfully!")


job = scheduler.add_job(
  validate_delivery, "cron", day_of_week="mon-fri", hour=12, end_date="2022-09-30"
)
job_1 = scheduler.add_job(
  sheet_update, "cron", day_of_week="mon-fri", hour=10, end_date="2022-09-30"
)
scheduler.start()

# job = scheduler.add_job(my_job, "interval", hours=24)