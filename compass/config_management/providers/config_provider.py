'''Provide Base class ConfigProvider for reading config.'''
import logging

from compass.utils import setting_wrapper as setting


class ConfigProvider(object):
    '''Base class for config provider.'''

    NAME = 'config_provider'

    def __init__(self):
        msg = '%s is not implemented' % self.__class__.__name__
        raise NotImplementedError(msg)

    def __repr__(self):
        return '%s[%s]' % (self.__class__.__name__, self.NAME)

    def getGlobalConfig(self):
        '''interface to read global config.'''
        return {}

    def getClusterConfig(self, clusterid):
        '''interface to read cluster config.'''
        return {}

    def getHostConfig(self, hostid):
        '''interface to read host config.'''
        return {}

    def getHostConfigs(self, hostids):
        '''get host configs.'''
        configs = {}
        for hostid in hostids:
            configs[hostid] = self.getHostConfig(hostid)
        return configs

    def updateGlobalConfig(self, config):
        '''interface to update global config.'''
        pass

    def updateClusterConfig(self, clusterid, config):
        '''interface to update cluster config.'''
        pass

    def updateHostConfig(self, hostid, config):
        '''interface to update host config.'''
        pass

    def updateHostConfigs(self, configs):
        '''update host configs.'''
        for hostname, config in configs.items():
            self.updateHostConfig(hostname, config)


PROVIDERS = {}


def getProvider():
    '''get default provider.'''
    return getProviderByName(setting.PROVIDER_NAME)


def getProviderByName(name):
    '''get provider by provider name.'''
    if name not in PROVIDERS:
        logging.error('provider name %s is not found in providers %s',
                      name, PROVIDERS)
        raise KeyError('provider %s is not found in PROVIDERS' % name)
    provider = PROVIDERS[name]()
    logging.debug('got provider %s', provider)
    return provider


def registerProvider(provider):
    '''register provider.'''
    if provider.NAME in PROVIDERS:
        logging.error('provider %s name %s is already registered in %s',
                      provider, provider.NAME, PROVIDERS)
        raise KeyError('provider %s is already registered in PROVIDERS' %
                       provider.NAME)
    logging.debug('register provider %s', provider.NAME)
    PROVIDERS[provider.NAME] = provider
