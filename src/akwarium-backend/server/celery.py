import os
import logging
from celery import Celery, signals

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

app = Celery("server")
app.config_from_object("django.conf:settings", namespace="CELERY")


@signals.celeryd_init.connect
def setup_log_format(sender, conf, **kwargs):
    conf.worker_log_format = '%(asctime)s %(levelname)s [%(name)s][%(processName)s]: %(message)s'
    conf.worker_task_log_format = (
        '%(asctime)s %(levelname)s [%(name)s][%(processName)s]'
        '[%(task_name)s(%(task_id)s)] %(message)s'
    )


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    return logging.getLogger('celery')
