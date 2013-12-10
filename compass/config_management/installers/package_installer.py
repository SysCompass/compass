'''Provider Base class for package installer.'''
import logging

from compass.config_management.installers import installer
from compass.utils import setting_wrapper as setting


class Installer(installer.Installer):
    '''Base class for package installer.'''
    NAME = 'package_installer'

    def getTargetSystems(self, oses):
        '''interface to get available target_systems for each os.
    
        Args:
            oses: list of str, supported oses.

        Returns:
           dict of {os_version: list of supported target system}
        '''
        return {}

    def getRoles(self, target_system):
        '''interface to get all roles of target system.

        Args:
            target_system: str, target cloud system such as openstack.

        Returns:
           dict of {role: description}
        ''' 
        return {}

    def os_installer_config(self, config, **kwargs):
        '''interface to get os installer related config.'''
        return {}


INSTALLERS = {}


def getInstallerByName(name):
    '''get package installer by name.'''
    if name not in INSTALLERS:
        logging.error('installer name %s is not in package installers %s',
                      name, INSTALLERS)
        raise KeyError('installer name %s is not in package INSTALLERS' % name)

    package_installer = INSTALLERS[name]()
    logging.debug('got package installer %s', package_installer)
    return package_installer


def register(package_installer):
    '''Register package installer.'''
    if package_installer.NAME in INSTALLERS:
        logging.error(
            'package installer %s is already in INSTALLERS %s',
            installer, INSTALLERS)
        raise KeyError(
            'package installer %s already registered' % package_installer)

    logging.debug('register package installer: %s', package_installer)
    INSTALLERS[package_installer.NAME] = package_installer


def getInstaller():
    '''get default package installer.'''
    return getInstallerByName(setting.PACKAGE_INSTALLER)
