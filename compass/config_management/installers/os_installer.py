'''provider Base class for os installer.'''
import logging

from compass.config_management.installers import installer
from compass.utils import setting_wrapper as setting


class Installer(installer.Installer):
    '''Base class for os installer.'''
    NAME = 'os_installer'

    def getOSes(self):
        '''interface to get supported oses.

        Returns:
            list of str, each is the supported os name and version.
        '''
        return []


INSTALLERS = {}


def getInstallerByName(name):
    '''Get os installer by name.'''
    if name not in INSTALLERS:
        logging.error('os installer name %s is not in os installers %s',
                      name, INSTALLERS)
        raise KeyError('os installer name %s is not in os INSTALLERS')

    os_installer = INSTALLERS[name]()
    logging.debug('got os installer %s', os_installer)
    return os_installer


def register(os_installer):
    '''Register os installer.'''
    if os_installer.NAME in INSTALLERS:
        logging.error(
            'os installer %s is already registered in INSTALLERS %s',
            os_installer, INSTALLERS)
        raise KeyError(
            'os installer %s is already registered' % os_installer)

    logging.debug('register os installer %s', os_installer)
    INSTALLERS[os_installer.NAME] = os_installer


def getInstaller():
    '''Get default os installer.'''
    return getInstallerByName(setting.OS_INSTALLER)
