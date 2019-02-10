from celery import Celery
from server import app
import os

CELERY_USERNAME = os.environ.get("CELERY_USERNAME")
CELERY_PASSWORD = os.environ.get("CELERY_PASSWORD")
MQ_HOST = os.environ.get("MQ_HOST")

def make_celery(app):
    # create context tasks in celery
    app.config["CELERY_BROKER_URL"] = f"amqp://{CELERY_USERNAME}:{CELERY_PASSWORD}@{MQ_HOST}"
    celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)
