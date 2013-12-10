'''config provider read config from file.'''
import json
import logging

from compass.config_management.providers import config_provider
from compass.utils import setting_wrapper as setting


class FileProvider(config_provider.ConfigProvider):
    '''config provider which reads config from file.'''
    NAME = 'file'

    def __init__(self):
        pass

    @classmethod
    def _globalConfigFilename(cls):
        '''Get global config file name.'''
        return '%s/%s' % (
            setting.CONFIG_DIR, setting.GLOBAL_CONFIG_FILENAME)

    @classmethod
    def _getConfigFormat(cls):
        '''Get config file format.'''
        return setting.CONFIG_FILE_FORMAT

    @classmethod
    def _configFormatIsPython(cls, config_format):
        '''Check if config file is stored as python formatted.'''
        if config_format == 'python':
            return True
        return False

    @classmethod
    def _configFormatIsJson(cls, config_format):
        '''Check if config file is stored as json formatted.'''
        if config_format == 'json':
            return True
        return False

    @classmethod
    def _readConfigFromFile(cls, filename, config_format):
        '''read config from file.'''
        config_globals = {}
        config_locals = {}
        content = ''
        try:
            with open(filename) as file_handler:
                content = file_handler.read()
        except Exception as error:
            logging.error('failed to read file %s', filename)
            logging.exception(error)
            return {}

        if cls._configFormatIsPython(config_format):
            try:
                exec(content, config_globals, config_locals)
            except Exception as error:
                logging.error('failed to exec %s', content)
                logging.exception(error)
                return {}

        elif cls._configFormatIsJson(config_format):
            try:
                config_locals = json.loads(content)
            except Exception as error:
                logging.error('failed to load json data %s', content)
                logging.exception(error)
                return {}

        return config_locals

    def getGlobalConfig(self):
        '''read global config from file.'''
        return self._readConfigFromFile(
            self._globalConfigFilename(),
            self._getConfigFormat())


config_provider.registerProvider(FileProvider)
