from celery import Celery
from django.apps import apps
from django.conf import settings

app = Celery("config", broker=settings.NOTIFICATION_CENTER_RABBITMQ)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
