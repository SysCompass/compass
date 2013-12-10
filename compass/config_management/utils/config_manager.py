'''
   Config Manager to get configs from providers and isntallers
   and update them to providers and installers.

   The working flow is:
       Get global config from provider (default from global config file).
       Get global config from os installer.
       Get global config from package installer.

       merge global config from global config got from provider,
       os installer, package installer.

       Update global config to provider (default no action).
       Update global config to os installer.
       Update global config to package installer.

       Get cluster config from provider (default from db).
       Get cluster config os installer.
       Get cluster config from package installer.

       merge cluster config from cluster config got from provider,
       os installer and package installer.

       merge global config into cluster config.

       Update cluster config to provider.
       Update cluster config to os installer.
       Update cluster config to package installer.

       Get hosts configs from provider (default from db)
       Get hosts configs from os installer.
       Get hosts configs from package installer.

       Call config_merger to update hosts configs from cluster config.

       Update hosts configs to provider.
       Update hosts configs to os installer.
       Update host configs to package installer.
'''
import functools
import logging

from compass.config_management.installers import os_installer
from compass.config_management.installers import package_installer
from compass.config_management.providers import config_provider
from compass.config_management.utils import config_merger_callbacks
from compass.config_management.utils.config_merger import ConfigMapping
from compass.config_management.utils.config_merger import ConfigMerger
from compass.utils import util


CLUSTER_HOST_MERGER = ConfigMerger(
    mappings=[
        ConfigMapping(
            path_list=['/networking/interfaces/*'],
            from_upper_keys={'ip_start': 'ip_start', 'ip_end': 'ip_end'},
            to_key='ip',
            value=config_merger_callbacks.assignIPs
        ),
        ConfigMapping(
            path_list=['/role_assign_policy'],
            from_upper_keys={
                'policy_by_host_numbers': 'policy_by_host_numbers',
                'default': 'default'},
            to_key='/roles',
            value=config_merger_callbacks.assignRolesByHostNumbers
        ),
        ConfigMapping(
            path_list=['/dashboard_roles'],
            from_lower_keys={'lower_values': '/roles'},
            to_key='/has_dashboard_roles',
            value=config_merger_callbacks.hasIntersection
        ),
        ConfigMapping(
            path_list=[
                '/networking/global',
                '/networking/interfaces/*/netmask',
                '/networking/interfaces/*/nic',
                '/networking/interfaces/*/promisc',
                '/security/*',
                '/partition',
            ]
        ),
        ConfigMapping(
            path_list=['/networking/interfaces/*'],
            from_upper_keys={'pattern': 'dns_pattern',
                             'clustername': '/clustername',
                             'search_path': '/networking/global/search_path'},
            from_lower_keys={'hostname': '/hostname'},
            to_key='dns_alias',
            value=functools.partial(config_merger_callbacks.assignFromPattern,
                                    upper_keys=['search_path', 'clustername'],
                                    lower_keys=['hostname'])
        ),
        ConfigMapping(
            path_list=['/networking/global'],
            from_upper_keys={'default': 'default_no_proxy'},
            from_lower_keys={'hostnames': '/hostname',
                             'ips': '/networking/interfaces/management/ip'},
            to_key='ignore_proxy',
            value=config_merger_callbacks.assignNoProxy
        )])


class ConfigManager(object):
    '''
       Config manger is to read global/clsuter/host configs from provider,
       os installer, package installer, process them.
       update them to provider, os installer, package installer.
    '''

    def __init__(self):
        self.config_provider = config_provider.getProvider()
        logging.debug('got config provider: %s', self.config_provider)
        self.os_installer = os_installer.getInstaller()
        logging.debug('got os installer: %s', self.os_installer)
        self.package_installer = package_installer.getInstaller()
        logging.debug('got package installer: %s', self.package_installer)

    def getAdapters(self):
        '''get adapter information from os installer and package installer.

        Returns:
            list of adapter information.
            For each adapter, the information is as:
                {
                    'name': 'CentOS/OpenStack',
                    'os': 'CentOS6.4',
                    'target_system': 'openstack'
                }
        '''
        oses = self.os_installer.getOSes()
        target_systems_per_os = self.package_installer.getTargetSystems(oses)
        adapters = []
        for os_version, target_systems in target_systems_per_os.items():
            for target_system in target_systems:
                adapters.append({
                    'name': '%s/%s' % (os_version, target_system),
                    'os': os_version,
                    'target_system': target_system})

        logging.debug('got adapters: %s', adapters)
        return adapters

    def getRoles(self, target_system):
        '''Get all roles of the target system from package installer.

        Args:
            target_system: str, the target cloud system such as openstack.

        Returns:
            list of role information.
            For each role, the information is as:
                {
                    'name': 'os-single-controller',
                    'description': 'openstack controller node',
                    'target_system': 'openstack'
                }
        '''
        roles = self.package_installer.getRoles(target_system)
        return [
            {
                'name': role,
                'description': description,
                'target_system': target_system
            } for role, description in roles.items()
        ]

    def getGlobalConfig(self, os_version, target_system):
        '''Get global config.'''
        config = self.config_provider.getGlobalConfig()
        logging.debug('got global provider config from %s: %s',
                      self.config_provider, config)

        os_config = self.os_installer.getGlobalConfig(
            os_version=os_version, target_system=target_system)
        logging.debug('got global os config from %s: %s',
                      self.os_installer, os_config)
        package_config = self.package_installer.getGlobalConfig(
            os_version=os_version,
            target_system=target_system)
        logging.debug('got global package config from %s: %s',
                      self.package_installer, package_config)

        util.mergeDict(config, os_config)
        util.mergeDict(config, package_config)
        logging.debug('got global config: %s', config)
        return config

    def updateGlobalConfig(self, config, os_version, target_system):
        '''update global config.'''
        logging.debug('update global config: %s', config)
        
        logging.debug('update global config to %s',
                      self.config_provider)
        self.config_provider.updateGlobalConfig(config)
        
        logging.debug('update global config to %s',
                      self.os_installer)
        self.os_installer.updateGlobalConfig(
            config, os_version=os_version, target_system=target_system)
        
        logging.debug('update global config to %s',
                      self.package_installer)
        self.package_installer.updateGlobalConfig(
            config, os_version=os_version, target_system=target_system)

    def getClusterConfig(self, clusterid, os_version, target_system):
        '''get cluster config.'''
        config = self.config_provider.getClusterConfig(clusterid)
        logging.debug('got cluster %s config from %s: %s',
                      clusterid, self.config_provider, config)

        os_config = self.os_installer.getClusterConfig(
            clusterid, os_version=os_version,
            target_system=target_system)
        logging.debug('got cluster %s config from %s: %s',
                      clusterid, self.os_installer, os_config)

        package_config = self.package_installer.getClusterConfig(
            clusterid, os_version=os_version,
            target_system=target_system)
        logging.debug('got cluster %s config from %s: %s',
                      clusterid, self.package_installer, package_config)
        
        util.mergeDict(config, os_config)
        util.mergeDict(config, package_config)
        logging.debug('got cluster %s config: %s', clusterid, config)
        return config

    def updateClusterConfig(self, clusterid, config, os_version, target_system):
        '''update cluster config.'''
        logging.debug('update cluster %s config: %s', clusterid, config)

        logging.debug('update cluster %s config to %s',
                      clusterid, self.config_provider)
        self.config_provider.updateClusterConfig(clusterid, config)

        logging.debug('update cluster %s config to %s',
                      clusterid, self.os_installer)
        self.os_installer.updateClusterConfig(
            clusterid, config, os_version=os_version,
            target_system=target_system)

        logging.debug('update cluster %s config to %s',
                      clusterid, self.package_installer)
        self.package_installer.updateClusterConfig(
            clusterid, config, os_version=os_version,
            target_system=target_system)

    def getHostConfig(self, hostid, os_version, target_system):
        '''get host config.'''
        config = self.config_provider.getHostConfig(hostid)
        logging.debug('got host %s config from %s: %s',
                      hostid, self.config_provider, config)

        os_config = self.os_installer.getHostConfig(
            hostid, os_version=os_version,
            target_system=target_system)
        logging.debug('got host %s config from %s: %s',
                      hostid, self.os_installer, os_config)

        package_config = self.package_installer.getHostConfig(
            hostid, os_version=os_version,
            target_system=target_system)
        logging.debug('got host %s config from %s: %s',
                      hostid, self.package_installer, package_config)

        util.mergeDict(config, os_config)
        util.mergeDict(config, package_config)
        logging.debug('got host %s config: %s', hostid, config)
        return config

    def getHostConfigs(self, hostids, os_version, target_system):
        '''get host configs.'''
        host_configs = {}
        for hostid in hostids:
            host_configs[hostid] = self.getHostConfig(
                hostid, os_version, target_system)
        return host_configs

    def updateHostConfig(self, hostid, config, os_version, target_system):
        'update host config.'''
        logging.debug('update host %s config: %s', hostid, config)

        logging.debug('update host %s config to %s',
                      hostid, self.config_provider)
        self.config_provider.updateHostConfig(hostid, config)

        logging.debug('update host %s config to %s',
                      hostid, self.os_installer)
        self.os_installer.updateHostConfig(
            hostid, config, os_version=os_version,
            target_system=target_system)

        logging.debug('update host %s config to %s',
                      hostid, self.package_installer)
        self.package_installer.updateHostConfig(
            hostid, config, os_version=os_version,
            target_system=target_system)

    def updateHostConfigs(self, host_configs, os_version, target_system):
        'update host configs.'''
        for hostid, host_config in host_configs.items():
            self.updateHostConfig(
                hostid, host_config, os_version, target_system)

    def updateClusterAndHostConfigs(self,
                                    clusterid,
                                    hostids,
                                    update_hostids,
                                    os_version,
                                    target_system):
        '''update cluster/host configs.'''
        logging.debug('update cluster %s with all hosts %s and update: %s',
                      clusterid, hostids, update_hostids)

        global_config = self.getGlobalConfig(os_version, target_system)
        self.updateGlobalConfig(global_config, os_version=os_version,
                                target_system=target_system)

        cluster_config = self.getClusterConfig(
            clusterid, os_version=os_version, target_system=target_system)
        util.mergeDict(cluster_config, global_config, False)
        self.updateClusterConfig(
            clusterid, cluster_config, os_version=os_version,
            target_system=target_system)

        host_configs = self.getHostConfigs(
            hostids, os_version=os_version,
            target_system=target_system)
        CLUSTER_HOST_MERGER.merge(cluster_config, host_configs)
        update_host_configs = dict(
            [(hostid, host_config)
             for hostid, host_config in host_configs.items()
             if hostid in update_hostids])
        self.updateHostConfigs(
            update_host_configs, os_version=os_version,
            target_system=target_system)

    def sync(self):
        '''
           Sync os installer and package installer to 
           catch up the latest change.
        '''
        self.os_installer.sync()
        self.package_installer.sync()
