from time import sleep

from src.tasks.celery_app import celery_instance


@celery_instance.task
def test_task():
    print('Task started')
    sleep(5)
    print('Task completed')