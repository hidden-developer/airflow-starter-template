from celery.signals import import_modules as celery_import_modules
from airflow.executors.celery_executor import (
    on_celery_import_modules as default_on_clery_import_modules,
)
from airflow.executors.celery_executor import *


@celery_import_modules.connect
def on_celery_import_modules(*args, **kwargs):
    default_on_clery_import_modules(*args, **kwargs)
    print("import on_celery_module")
