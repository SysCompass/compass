'''Module to provider base installer class Installer.'''


class Installer(object):
    '''Base class for installer.'''
    NAME = 'installer'

    def __init__(self):
        raise NotImplementedError(
            '%s is not implemented' % self.__class__.__name__)

    def __repr__(self):
        return '%s[%s]' % (self.__class__.__name__, self.NAME)

    def sync(self):
        '''interface to sync installer.'''
        pass

    def getGlobalConfig(self, **kwargs):
        '''interface to get global config.'''
        return {}

    def getClusterConfig(self, clusterid, **kwargs):
        '''interface to get cluster config.'''
        return {}

    def getHostConfig(self, hostid, **kwargs):
        '''interface to get host config.'''
        return {}

    def getHostConfigs(self, hostids, **kwargs):
        '''get host configs.'''
        host_configs = {}
        for hostid in hostids:
            host_configs[hostid] = self.getHostConfig(hostid, **kwargs)
        return host_configs

    def updateGlobalConfig(self, config, **kwargs):
        '''interface to update global config.'''
        pass

    def updateClusterConfig(self, clusterid, config, **kwargs):
        '''interface to update cluster config.'''
        pass

    def updateHostConfig(self, hostid, config, **kwargs):
        '''interface to update host config.'''
        pass

    def updateHostConfigs(self, host_configs, **kwargs):
        '''updaet host configs.'''
        for hostid, config in host_configs.items():
            self.updateHostConfig(hostid, config, **kwargs)
