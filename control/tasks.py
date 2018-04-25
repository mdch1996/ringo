from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

from .utils import check_ip, check_door_opening


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="task_check_ip",
    ignore_result=True
)
def task_check_ip():
    check_ip()


@shared_task
def task_check_door_opening():

    print('---------task_check_door_opening()--------')

    while True:
        check_door_opening()
