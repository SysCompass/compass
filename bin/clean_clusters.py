#!/usr/bin/python
import logging
import os.path
import shutil

from compass.config_management.utils import config_manager
from compass.db import database
from compass.db.model import Adapter, Cluster, ClusterHost
from compass.db.model import ClusterState, HostState
from compass.db.model import LogProgressingHistory
from compass.utils import flags
from compass.utils import logsetting
from compass.utils import setting_wrapper as setting


flags.add('clusters',
          help=(
              'clusters to clean, the format is as '
              'clusterid:hostname1,hostname2,...;...'),
          default='')


def clean_clusters():
    """function to clean cluster and hosts configuration."""
    clusters = {}
    for clusterid_and_hostnames in flags.OPTIONS.clusters.split(';'):
        if not clusterid_and_hostnames:
            continue

        clusterid_str, hostnames_str = clusterid_and_hostnames.split(':', 1)
        clusterid = int(clusterid_str)
        hostnames = [
            hostname for hostname in hostnames_str.split(',')
            if hostname
        ]

    manager = config_manager.ConfigManager()
    with database.session() as session:
        clusterids = clusters.keys()
        if not clusterids:
            cluster_list = session.query(Cluster).all()
            clusterids = [cluster.id for cluster in cluster_list]

        for clusterid in clusterids:
            hostnames = clusters.get(clusterid, [])
            if not hostnames:
                host_list = session.query(ClusterHost).filter_by(
                    cluster_id=clusterid).all()
                hostids = [host.id for host in host_list]
                clusters[clusterid] = hostids
            else:
                hostids = []
                for hostname in hostnames:
                    host = session.query(ClusterHost).filter_by(
                        cluster_id=clusterid, hostname=hostname).first()
                    if host:
                        hostids.append(host.id)
                clusters[clusterid] = hostids

        logging.info('clean cluster hosts: %s', clusters)
        for clusterid, hostids in clusters.items():
            cluster = session.query(Cluster).filter_by(id=clusterid).first()
            if not cluster:
                continue

           
            all_hostids = [host.id for host in cluster.hosts]
            logging.debug('all hosts in cluster %s is: %s',
                          clusterid, all_hostids)

            logging.info('clean hosts %s in cluster %s',
                         hostids, clusterid)
            adapter = cluster.adapter
            for hostid in hostids:
                host = session.query(ClusterHost).filter_by(id=hostid).first()
                if not host:
                    continue

                log_dir = os.path.join(
                    setting.INSTALLATION_LOGDIR,
                    '%s.%s' % (host.hostname, clusterid))
                logging.info('clean log dir %s', log_dir)
                shutil.rmtree(log_dir, True)
                session.query(LogProgressingHistory).filter(
                    LogProgressingHistory.pathname.startswith(
                        '%s/' % log_dir)).delete(
                    synchronize_session='fetch')

                logging.info('clean host %s', hostid)
                manager.clean_host_config(
                    hostid,
                    os_version=adapter.os,
                    target_system=adapter.target_system)
                session.query(ClusterHost).filter_by(
                    id=hostid).delete(synchronize_session='fetch')
                session.query(HostState).filter_by(
                    id=hostid).delete(synchronize_session='fetch')

            if set(all_hostids) == set(hostids):
                logging.info('clean cluster %s', clusterid)
                manager.clean_cluster_config(
                    clusterid,
                    os_version=adapter.os,
                    target_system=adapter.target_system)
                session.query(Cluster).filter_by(
                    id=clusterid).delete(synchronize_session='fetch')
                session.query(ClusterState).filter_by(
                    id=clusterid).delete(synchronize_session='fetch')


if __name__ == '__main__':
    flags.init()
    logsetting.init()
    clean_clusters() 
