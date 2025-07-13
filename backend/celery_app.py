from celery import Celery

celery = Celery(
    'parking-app',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0',
    include=['tasks']
)