'''Module to define celery tasks.'''
from celery.signals import setup_logging

from compass.actions import poll_switch
from compass.actions import trigger_install
from compass.actions import progress_update
from compass.db import database
from compass.tasks.client import celery
from compass.utils import flags
from compass.utils import logsetting
from compass.utils import setting_wrapper as setting


def tasks_setup_logging(**_kw):
    '''setup logging options'''
    flags.init()
    flags.OPTIONS.logfile = setting.CELERY_LOGFILE
    logsetting.init()


setup_logging.connect(tasks_setup_logging)


@celery.task(name="compass.tasks.pollswitch")
def pollswitch(ip_addr, req_obj='mac', oper="SCAN"):
    """ Query switch and return expected result.

        :param str ip_addr     : switch ip address
        :param str reqObj      : the object requested to query from switch
        :param str oper        : the operation to query the switch
                                 (SCAN, GET, SET)
    """
    with database.session():
        poll_switch.poll_switch(ip_addr, req_obj='mac', oper="SCAN")


@celery.task(name="compass.tasks.trigger_install")
def triggerInstall(clusterid):
    """Trigger install progress for the given cluster.

    Args:
        clusterid: int. Used to query a host table to get host
                    configurations.

    Returns:
        None
    """
    with database.session():
        trigger_install.trigger_install(clusterid)


@celery.task(name="compass.tasks.progress_update")
def progressUpdate(clusterid):
    """Calculate the installing progress of given cluster.

    Args:
        clusterid: int, to updte installing progress of the cluster.

    Returns:
        None
    """
    progress_update.updateProgress(clusterid)
