'''module to update progress bar of the given cluster.'''
import logging

from compass.db import database
from compass.db.model import Cluster
from compass.log_analyzor import file_matcher
from compass.log_analyzor import progress_calculator
from compass.utils import setting_wrapper as setting


def updateProgress(clusterid):
    '''update progress bar for the given cluster.

    Args:
        clusterid: int, the id of the cluster.
    
    Returns:
        None.

    The function should be called out of the database session scope.
    In the function, it will update the database cluster_state and
    host_state table. The frontend will get the updated instaling state
    and progress from the two tables.
    The function will also query log_progressing_history table to get
    the lastest installing progress and the position of log it has processed
    in the last run. The function uses these information to avoid recalculate
    the progress from the beginning of the log file. After the progress got
    updated, it stores the information to the log_progressing_history for
    next time run.
    '''
    os_version = ''
    hostids = []
    with database.session() as session:
        cluster = session.query(Cluster).filter_by(id=clusterid).first()
        if not cluster:
            logging.error('no cluster found for %s', clusterid)
            return

        if not cluster.adapter:
            logging.error('there is no adapter for cluster %s', clusterid)
            return

        os_version = cluster.adapter.os
        if not cluster.state:
            logging.error('there is no state for cluster %s', clusterid)
            return

        if cluster.state.state != 'INSTALLING':
            logging.error('the state %s is not in installing for cluster %s',
                          cluster.state.state, clusterid)
            return

        hostids = [host.id for host in cluster.hosts]

    progress_calculator.updateProgress(os_version,
                                       setting.PACKAGE_INSTALLER,
                                       clusterid, hostids)
