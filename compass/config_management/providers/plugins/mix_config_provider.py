'''mix provider which read config from different other providers.'''
from compass.config_management.providers import config_provider
from compass.utils import setting_wrapper as setting


class MixProvider(config_provider.ConfigProvider):
    '''mix provider which read config from different other providers.'''
    NAME = 'mix'

    def __init__(self):
        self.global_provider = config_provider.getProviderByName(
            setting.GLOBAL_CONFIG_PROVIDER)
        self.cluster_provider = config_provider.getProviderByName(
            setting.CLUSTER_CONFIG_PROVIDER)
        self.host_provider = config_provider.getProviderByName(
            setting.HOST_CONFIG_PROVIDER)

    def getGlobalConfig(self):
        '''get global config.'''
        return self.global_provider.getGlobalConfig()

    def getClusterConfig(self, clusterid):
        '''get cluster config.'''
        return self.cluster_provider.getClusterConfig(clusterid)

    def getHostConfig(self, hostid):
        '''get host config.'''
        return self.host_provider.getHostConfig(hostid)

    def updateGlobalConfig(self, config):
        '''update global config.'''
        self.global_provider.updateGlobalConfig(config)

    def updateClusterConfig(self, clusterid, config):
        '''update cluster config.'''
        self.cluster_provider.updateClusterConfig(
            clusterid, config)

    def updateHostConfig(self, hostid, config):
        '''update host config.'''
        self.host_provider.updateHostConfig(hostid, config)


config_provider.registerProvider(MixProvider)
