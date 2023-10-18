from celery import Celery
from celery.schedules import crontab
from src.config import REDIS_HOST, REDIS_PORT
from src.handlers.misc import post_on_channel


celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


@celery.task
async def post():
    await post_on_channel()


celery.conf.beat_schedule = {
    'task-name': {
        'task': 'tasks.post',  # instead 'post'
        'schedule': crontab(minute='*/30', hour='9-23'),
    },
}


celery.conf.timezone = 'Europe/Moscow'
