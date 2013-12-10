'''cobbler plugins as os installer.'''
import functools
import logging
import xmlrpclib

from compass.config_management.installers import os_installer
from compass.config_management.installers import package_installer
from compass.config_management.utils.config_translator import ConfigTranslator
from compass.config_management.utils.config_translator import KeyTranslator
from compass.config_management.utils import config_translator_callbacks
from compass.utils import setting_wrapper as setting
from compass.utils import util


TO_HOST_TRANSLATOR = ConfigTranslator(
    mapping={
        '/networking/global/gateway': [KeyTranslator(
            translated_keys=['/gateway']
        )],
        '/networking/global/nameservers': [KeyTranslator(
            translated_keys=['/name_servers']
        )],
        '/networking/global/search_path': [KeyTranslator(
            translated_keys=['/name_servers_search']
        )],
        '/networking/global/proxy': [KeyTranslator(
            translated_keys=['/ksmeta/proxy']
        )],
        '/networking/global/ignore_proxy': [KeyTranslator(
            translated_keys=['/ksmeta/ignore_proxy']
        )],
        '/networking/global/ntp_server': [KeyTranslator(
            translated_keys=['/ksmeta/ntp_server']
        )],
        '/security/server_credentials/username': [KeyTranslator(
            translated_keys=['/ksmeta/username']
        )],
        '/security/server_credentials/password': [KeyTranslator(
            translated_keys=['/ksmeta/password'],
            translated_value=config_translator_callbacks.getEncryptedValue
        )],
        '/partition': [KeyTranslator(
            translated_keys=['/ksmeta/partition']
        )],
        '/networking/interfaces/*/mac': [KeyTranslator(
            translated_keys=[functools.partial(
                config_translator_callbacks.getKeyFromPattern,
                to_pattern='/modify_interface/macaddress-%(nic)s')],
            from_keys={'nic': '../nic'},
            override=functools.partial(
                config_translator_callbacks.overridePathHas,
                should_exist='management')
        )],
        '/networking/interfaces/*/ip': [KeyTranslator(
            translated_keys=[functools.partial(
                config_translator_callbacks.getKeyFromPattern,
                to_pattern='/modify_interface/ipaddress-%(nic)s')],
            from_keys={'nic': '../nic'},
            override=functools.partial(
                config_translator_callbacks.overridePathHas,
                should_exist='management')
        )],
        '/networking/interfaces/*/netmask': [KeyTranslator(
            translated_keys=[functools.partial(
                config_translator_callbacks.getKeyFromPattern,
                to_pattern='/modify_interface/netmask-%(nic)s')],
            from_keys={'nic': '../nic'},
            override=functools.partial(
                config_translator_callbacks.overridePathHas,
                should_exist='management')
        )],
        '/networking/interfaces/*/dns_alias': [KeyTranslator(
            translated_keys=[functools.partial(
                config_translator_callbacks.getKeyFromPattern,
                to_pattern='/modify_interface/dnsname-%(nic)s')],
            from_keys={'nic': '../nic'},
            override=functools.partial(
                config_translator_callbacks.overridePathHas,
                should_exist='management')
        )],
        '/networking/interfaces/*/nic': [KeyTranslator(
            translated_keys=[functools.partial(
                config_translator_callbacks.getKeyFromPattern,
                to_pattern='/modify_interface/static-%(nic)s')],
            from_keys={'nic': '../nic'},
            translated_value=True,
            override=functools.partial(
                config_translator_callbacks.overridePathHas,
                should_exist='management'),
        ), KeyTranslator(
            translated_keys=[functools.partial(
                config_translator_callbacks.getKeyFromPattern,
                to_pattern='/modify_interface/management-%(nic)s')],
            from_keys={'nic': '../nic'},
            translated_value=functools.partial(
                config_translator_callbacks.overridePathHas,
                should_exist='management'),
            override=functools.partial(
                config_translator_callbacks.overridePathHas,
                should_exist='management')
        ), KeyTranslator(
            translated_keys=['/ksmeta/promisc_nics'],
            from_values={'condition': '../promisc'},
            translated_value=config_translator_callbacks.addValue,
            override=True,
        )],
    }
)


class Installer(os_installer.Installer):
    '''cobbler installer'''
    NAME = 'cobbler'

    def __init__(self):
        # the connection is created when cobbler installer is initialized.
        try:
            self.remote = xmlrpclib.Server(
                setting.COBBLER_INSTALLER_URL,
                allow_none=True)
            self.token = self.remote.login(
                *setting.COBBLER_INSTALLER_TOKEN)
        except Exception as error:
            logging.error('failed to login %s with (user, password) %s',
                          setting.COBBLER_INSTALLER_URL,
                          setting.COBBLER_INSTALLER_TOKEN)
            logging.exception(error)
            raise error

        # cobbler tries to get package related config from package installer.
        self.package_installer = package_installer.getInstaller()
        logging.debug('%s instance created: %s', self.NAME, self)

    def __str__(self):
        return (
            'remote:%s, token:%s, package_installer:%s') % (
                self.remote, self.token,
                self.package_installer)

    def getOSes(self):
        '''get supported os versions.
        
        In cobbler, we treat profile name as the indicator
        of supported os version. It is just a simple indicator
        and is not so accurate.
        '''
        profiles = self.remote.get_profiles()
        oses = []
        for profile in profiles:
            oses.append(profile['name'])
        return oses

    def sync(self):
        '''sync cobbler to catch up the latest update config.'''
        logging.debug('sync %s', self)
        try:
            self.remote.sync(self.token)
        except Exception as error:
            logging.error('failed to sync configs to %s',
                          self)
            logging.exception(error)

    def _getModifySystemFromConfig(self, hostname,
                                   profile, config, **kwargs):
        '''get modified system config.'''
        logging.debug('%s[%s] get modify system from config: %s',
                      self, hostname, config)
        system_config = {
            'name': hostname,
            'hostname': hostname,
            'profile': profile,
        }

        translated_config = TO_HOST_TRANSLATOR.translate(config)
        logging.debug('%s[%s] get translated config: %s',
                      self.NAME, hostname, translated_config)
        util.mergeDict(system_config, translated_config)

        ksmeta = system_config.setdefault('ksmeta', {})
        package_config = {'tool': self.package_installer.NAME}
        util.mergeDict(
            package_config,
            self.package_installer.os_installer_config(
                config, **kwargs))
        logging.debug('%s[%s] get package config: %s',
                      self.NAME, hostname, package_config)
        util.mergeDict(ksmeta, package_config)

        return system_config

    def _getProfile(self, **kwargs):
        '''get profile name.'''
        try:
            os_version = kwargs['os_version']
            profile_found = self.remote.find_profile(
                {'name': os_version})
            return profile_found[0]
        except Exception as error:
            logging.error('%s failed to found profile from %s',
                          self, kwargs)
            logging.exception(error)
            return None

    def _getSystem(self, hostid, config):
        '''get system reference id.'''
        try:
            hostname = config['hostname']
            sys_found = self.remote.find_system(
                {"hostname": hostname})

            if sys_found:
                sys_id = self.remote.get_system_handle(
                    sys_found[0], self.token)
                logging.debug('using existing system %s from %s',
                              sys_id, sys_found)
            else:
                sys_id = self.remote.new_system(self.token)
                logging.debug('create new system %s', sys_id)
            return (hostname, sys_id)
        except Exception as error:
            logging.error('%s failed to get system config for %s',
                          self, hostid)
            logging.exception(error)
            return (None, None)

    def _saveSystem(self, sys_id):
        '''save system config update.'''
        try:
            self.remote.save_system(sys_id, self.token)
        except Exception as error:
            logging.error(
                '%s failed to save config to %s',
                self, sys_id)
            logging.exception(error)

    def _updateModifySystem(self, sys_id, system_config):
        '''update modify system'''
        for key, value in system_config.items():
            try:
                self.remote.modify_system(
                    sys_id, key, value, self.token)
            except Exception as error:
                logging.error(
                    '%s failed to update config to %s[%s]: %s',
                    self, sys_id, key, value)
                logging.exception(error)

    def updateHostConfig(self, hostid, config, **kwargs):
        '''update host config.'''
        profile = self._getProfile(**kwargs)
        hostname, sys_id = self._getSystem(hostid, config)
        if profile is None or sys_id is None:
            return

        system_config = self._getModifySystemFromConfig(
            hostname, profile, config, **kwargs)
        logging.debug('%s system config to update: %s',
                      hostid, system_config)

        self._updateModifySystem(sys_id, system_config)
        self._saveSystem(sys_id)



os_installer.register(Installer)
