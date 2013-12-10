'''Module to setup celery client.'''
import os

from celery import Celery


celery = Celery(__name__)
if 'CELERY_CONFIG_MODULE' in os.environ:
    celery.config_from_envvar('CELERY_CONFIG_MODULE')
else:
    from compass.utils import celeryconfig_wrapper as celeryconfig
    celery.config_from_object(celeryconfig)
