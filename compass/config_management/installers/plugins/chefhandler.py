'''plugin module for chef as package instaler.'''
import fnmatch
import logging

from compass.utils import util
from compass.config_management.installers import package_installer
from compass.config_management.utils.config_translator import ConfigTranslator
from compass.config_management.utils.config_translator import KeyTranslator
from compass.config_management.utils import config_translator_callbacks
from compass.utils import setting_wrapper as setting


TO_CLUSTER_TRANSLATORS = {
    'openstack': ConfigTranslator(
        mapping={
            '/security/console_credentials': [KeyTranslator(
                translated_keys=['credential/identity/users/admin'],
            )],
            '/security/service_credentials': [KeyTranslator(
                translated_keys=[
                    '/credential/identity/users/compute',
                    '/credential/identity/users/image',
                    '/credential/identity/users/metering',
                    '/credential/identity/users/network',
                    '/credential/identity/users/object-store',
                    '/credential/identity/users/volume',
                    '/credential/mysql/compute',
                    '/credential/mysql/dashboard',
                    '/credential/mysql/identity',
                    '/credential/mysql/image',
                    '/credential/mysql/metering',
                    '/credential/mysql/network',
                    '/credential/mysql/super',
                    '/credential/mysql/volume',
                ]
            )],
            '/networking/interfaces/management/nic': [KeyTranslator(
                translated_keys=['/networking/control/interface'],
            )],
            '/networking/global/ntp_server': [KeyTranslator(
                translated_keys=['/ntp/ntpserver']
            )],
            '/networking/interfaces/storage/nic': [KeyTranslator(
                translated_keys=['/networking/storage/interface']
            )],
            '/networking/interfaces/public/nic': [KeyTranslator(
                translated_keys=['/networking/public/interface']
            )],
            '/networking/interfaces/tenant/nic': [KeyTranslator(
                translated_keys=['/networking/tenant/interface']
            )],
        }
    ),
}


FROM_CLUSTER_TRANSLATORS = {
    'openstack': ConfigTranslator(
        mapping={
            '/role_assign_policy': [KeyTranslator(
                translated_keys=['/role_assign_policy']
            )],
            '/dashboard_roles': [KeyTranslator(
                translated_keys=['/dashboard_roles']
            )],
        }
    ),
}


TO_HOST_TRANSLATORS = {
    'openstack': ConfigTranslator(
        mapping={
            '/networking/interfaces/management/ip': [KeyTranslator(
                translated_keys=[
                    '/db/mysql/bind_address',
                    '/mq/rabbitmq/bind_address',
                    '/endpoints/compute/metadata/host',
                    '/endpoints/compute/novnc/host',
                    '/endpoints/compute/service/host',
                    '/endpoints/compute/xvpvnc/host',
                    '/endpoints/ec2/admin/host',
                    '/endpoints/ec2/service/host',
                    '/endpoints/identity/admin/host',
                    '/endpoints/identity/service/host',
                    '/endpoints/image/registry/host',
                    '/endpoints/image/service/host',
                    '/endpoints/metering/service/host',
                    '/endpoints/network/service/host',
                    '/endpoints/volume/service/host',
                ],
                translated_value=config_translator_callbacks.getValueIf,
                from_values={'condition': '/has_dashboard_roles'}
            )],
        }
    ),
}


class Installer(package_installer.Installer):
    '''chef package installer.'''
    NAME = 'chef'

    @classmethod
    def installer_url(cls):
        '''get chef server url.'''
        return setting.CHEF_INSTALLER_URL

    @classmethod
    def global_databag_name(cls):
        '''get global databag name'''
        return setting.CHEF_GLOBAL_DATABAG_NAME

    @classmethod
    def cluster_databag_name(cls, clusterid, target_system):
        '''get cluster databag name'''
        return '%s_%s' % (target_system, str(clusterid))

    def os_installer_config(self, config, **kwargs):
        '''get os installer config.'''
        target_system = kwargs['target_system']
        clusterid = config.get('clusterid', 0)
        roles = config.get('roles', [])
        return {
            '%s_url' % self.NAME: self.installer_url(),
            'run_list': ','.join(
                ['"role[%s]"' % role for role in roles if role]),
            'cluster_databag': self.cluster_databag_name(
                clusterid, target_system),
        }

    def getTargetSystems(self, oses):
        '''get target systems.'''
        from chef import DataBag
        try:
            databags = DataBag.list(api=self.api)
        except Exception as error:
            logging.error('%s failed to get the databags', self.NAME)
            logging.exception(error)
            raise error

        target_systems = {}
        for os_version in oses:
            target_systems[os_version] = []

        for databag in databags:
            target_system = databag
            global_databag_item = self.getGlobalDataBagItem(
                self.getDataBag(target_system))
            support_oses = global_databag_item.get('support_oses', [])
            for os_version in oses:
                for support_os in support_oses:
                    if fnmatch.fnmatch(os_version, support_os):
                        target_systems[os_version].append(target_system)
                        break

        return target_systems

    def getRoles(self, target_system):
        '''get supported roles.'''
        global_databag_item = self.getGlobalDataBagItem(
            self.getDataBag(target_system))
        return global_databag_item.get('all_roles', {})

    def __init__(self):
        import chef
        try:
            self.api = chef.autoconfigure()
        except Exception as error:
            logging.error('%s failed to autoconfigure', self.NAME)
            logging.exception(error)
            raise error
        logging.debug('%s instance created %s', self.NAME, self.api)

    def getDataBag(self, target_system):
        '''get databag.'''
        from chef import DataBag
        try:
            return DataBag(target_system, api=self.api)
        except Exception as error:
            logging.error('%s failed to get databag of %s',
                          self.NAME, target_system)
            logging.exception(error)
            raise error

    def getDataBagItem(self, bag, bag_item_name):
        '''get databag item.'''
        from chef import DataBagItem
        try:
            return DataBagItem(bag, bag_item_name, api=self.api)
        except Exception as error:
            logging.error('%s failed to get bag item %s from %s',
                          self.NAME, bag_item_name, bag)
            logging.exception(error)
            raise error

    def getGlobalDataBagItem(self, bag):
        '''get global databag item.'''
        return self.getDataBagItem(
            bag, self.global_databag_name())

    def getClusterDataBagItem(self, bag, clusterid, target_system):
        '''get cluster databag item.'''
        return self.getDataBagItem(
            bag, self.cluster_databag_name(clusterid, target_system))

    def getClusterConfig(self, clusterid, **kwargs):
        '''get cluster config.'''
        target_system = kwargs['target_system']
        if target_system not in FROM_CLUSTER_TRANSLATORS:
            return {}

        bag = self.getDataBag(target_system)
        global_bag_item = dict(self.getGlobalDataBagItem(bag))
        bag_item = dict(self.getClusterDataBagItem(
            bag, clusterid, target_system))
        util.mergeDict(bag_item, global_bag_item, False)

        return FROM_CLUSTER_TRANSLATORS[target_system].translate(bag_item)

    def updateClusterConfig(self, clusterid, config, **kwargs):
        '''update cluster config.'''
        target_system = kwargs['target_system']
        bag = self.getDataBag(target_system)
        global_bag_item = dict(self.getGlobalDataBagItem(bag))
        bag_item = self.getClusterDataBagItem(bag, clusterid, target_system)
        bag_item_dict = dict(bag_item)
        util.mergeDict(bag_item_dict, global_bag_item, False)

        if target_system not in TO_CLUSTER_TRANSLATORS:
            return
        
        translated_config = TO_CLUSTER_TRANSLATORS[target_system].translate(
            config)
        util.mergeDict(bag_item_dict, translated_config)

        for key, value in bag_item_dict.items():
            bag_item[key] = value

        bag_item.save()

    def updateHostConfig(self, hostid, config, **kwargs):
        '''update host cnfig.'''
        target_system = kwargs['target_system']
        clusterid = config['clusterid']
        bag = self.getDataBag(target_system)
        global_bag_item = dict(self.getGlobalDataBagItem(bag))
        bag_item = self.getClusterDataBagItem(bag, clusterid, target_system)
        bag_item_dict = dict(bag_item)
        util.mergeDict(bag_item_dict, global_bag_item, False)

        if target_system not in TO_HOST_TRANSLATORS:
            return
            
        translated_config = TO_HOST_TRANSLATORS[target_system].translate(
            config)
        util.mergeDict(bag_item_dict, translated_config)

        for key, value in bag_item_dict.items():
            bag_item[key] = value

        bag_item.save()


package_installer.register(Installer)
