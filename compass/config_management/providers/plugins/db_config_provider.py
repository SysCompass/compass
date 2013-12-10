'''config provider read config from db.'''
from compass.config_management.providers import config_provider
from compass.config_management.utils import config_filter
from compass.db import database
from compass.db.model import Cluster, ClusterHost


CLUSTER_ALLOWS = ['*']
CLUSTER_DENIES = []
HOST_ALLOWS = ['*']
HOST_DENIES = []


class DBProvider(config_provider.ConfigProvider):
    '''config provider which reads config from db.'''
    NAME = 'db'
    CLUSTER_FILTER = config_filter.ConfigFilter(CLUSTER_ALLOWS, CLUSTER_DENIES)
    HOST_FILTER = config_filter.ConfigFilter(HOST_ALLOWS, HOST_DENIES)

    def __init__(self):
        pass

    def getClusterConfig(self, clusterid):
        '''get cluster config from db.'''
        session = database.current_session()
        cluster = session.query(Cluster).filter_by(id=clusterid).first()
        if cluster:
            return cluster.config
        else:
            return {}

    def getHostConfig(self, hostid):
        '''get host config from db.'''
        session = database.current_session()
        host = session.query(ClusterHost).filter_by(id=hostid).first()
        if host:
            return host.config
        else:
            return {}

    def updateHostConfig(self, hostid, config):
        '''update hsot config to db.'''
        session = database.current_session()
        host = session.query(ClusterHost).filter_by(id=hostid).first()
        if not host:
            return
        filtered_config = self.HOST_FILTER.filter(config)
        host.config = filtered_config


config_provider.registerProvider(DBProvider)
