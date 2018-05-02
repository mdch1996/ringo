from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

from . import utils


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_check_ip",
    ignore_result=True
)
def task_check_ip():
    utils.check_ip()
