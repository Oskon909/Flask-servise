
from celery import Celery
from celery.schedules import crontab

# from app import logger


def make_celery(app):
    #Celery configuration
    app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
    app.config['CELERYBEAT_SCHEDULE'] = {
        # Executes every minute
        # 'periodic_task-every-minute': {
        #     'task': 'periodic_task',
        #     'schedule': crontab(minute="*")
        # },
        # 'periodic_task-every-1-minutes': {
        #     'task': 'periodic_task2',
        #     'schedule': crontab(hour="*")
        # },
    }

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


