'''module to trigger the install progress for a given cluster.'''
import logging

from compass.db import database
from compass.db.model import Cluster, ClusterState, HostState
from compass.config_management.utils.config_manager import ConfigManager


def trigger_install(clusterid):
    '''trigger installer to start install for a given cluster.

    Args:
        clusterid: int, the id of the cluster.

    Returns:
        None
    '''
    manager = ConfigManager()
    session = database.current_session()
    cluster = session.query(Cluster).filter_by(id=clusterid).first()
    if not cluster:
        logging.error('no cluster found for %s', clusterid)
        return

    if not cluster.state:
        cluster.state = ClusterState()

    if cluster.state.state and cluster.state.state != 'UNINITIALIZED':
        logging.error('ignore installing cluster %s since the state is %s',
                      cluster.id, cluster.state)
        return

    cluster.state.state = 'INSTALLING'
    session.flush()
    adapter = cluster.adapter
    if not adapter:
        logging.error('no proper adapter found for cluster %s', cluster.id)
        return

    hostids = [host.id for host in cluster.hosts]
    update_hostids = []
    for host in cluster.hosts:
        if not host.state:
            host.state = HostState()
        elif host.state.state and host.state.state != 'UNINITIALIZED':
            logging.info('ignore installing host %s sinc eth state is %s',
                         host.id, host.state)
            continue

        host.state.state = 'INSTALLING'
        update_hostids.append(host.id)

    manager.updateClusterAndHostConfigs(clusterid, hostids, update_hostids,
                                        adapter.os, adapter.target_system)
    manager.sync()
