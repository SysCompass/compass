'''Config Translator module to translate orign config to dest config.
'''
import logging

from compass.config_management.utils import config_reference
from compass.utils import util


class KeyTranslator(object):
    '''
       Translate refs to the path in origin config to
       expected position in dest config. 

    Example:
        config = {
            'networking': {
                'management': {
                    'ip': '1.2.3.4',
                    'nic': 'eth0',
                },
                'public': {
                    'ip': '2.3.4.5',
                    'nic': 'eth0',
                },
            },
            'security': {
                'user': 'root',
                'password': 'root',
            },
        }
        ref = ConfigReference(config)
        translated_ref = ConfigReference({})
        translator = KeyTranslator(
            translated_keys=[
                functools.partial(
                    config_translator_callbacks.getKeyFromPattern,
                    to_pattern='/modify_interface/ipaddress-%(nic)s'),
                ),
            ],
            from_keys={'nic': '../nic'},
            override=functools.partial(
                config_translator_callbacks.overridePathHas,
                should_exist='management')
        )
        translator.translte(ref, '/networking/*/ip', translated_ref)
        translated_ref.config == {
            'modify_interface': {
                'ipaddress-eth0': '1.2.3.4',
            },
        }
        translator = KeyTranslator(
            translated_keys=[functools.partial(
                config_translator_callbacks.getKeyFromPattern,
                to_pattern='/modify_interface/static-%(nic)s')],
            from_keys={'nic': '../nic'},
            translated_value=True,
            override=functools.partial(
                config_translator_callbacks.overridePathHas,
                should_exist='management'),
        )
        translator.translate(ref, '/networking/*/nic', translated_ref)
        translated_ref.config == {
            'modify_interface': {
                'ipaddress-eth0': '1.2.3.4',
                'static-eth0': True 
            },
        }
        translator = KeyTranslator(
            translated_keys=['/ksmeta/username'] 
        )
        translator.translate(ref, '/security/user', translated_ref)
        translated_ref.config == {
            'modify_interface': {
                'ipaddress-eth0': '1.2.3.4',
                'static-eth0': True 
            },
            'ksmeta': {
                'username': 'root',
            },
        }
    '''
    def __init__(self, translated_keys=[], from_keys={}, translated_value=None,
                 from_values={}, override=False, override_conditions={}):
        self.translated_keys = translated_keys
        self.from_keys = from_keys
        self.translated_value = translated_value
        self.from_values = from_values
        self.override = override
        self.override_conditions = override_conditions
        self.isValid()

    def _isValidTranslatedKeys(self):
        '''Check translated keys are valid.'''
        for i, translated_key in enumerate(self.translated_keys):
            if util.isInstanceOf(translated_key, [str, unicode]):
                if '*' in translated_key:
                    raise KeyError(
                        'transalted_keys[%d] %s should not contain *' % (
                            i, translated_key))
            elif not callable(translated_key):
                raise TypeError(
                    'translated_keys[%d] type is %s while expected '
                     'types are str or callable: %s' % (
                         i, type(translated_key), translated_key))

    def _isValidFromKeys(self):
        '''Check from keys are valid.'''
        for mapping_key, from_key in self.from_keys.items():
            if not util.isInstanceOf(from_key, [str, unicode]):
                raise TypeError(
                    'from_keys[%s] type is %s while '
                    'expected type is [str, unicode]: %s' % (
                        mapping_key, type(from_key), from_key))
            
            if '*' in from_key:
                raise KeyError(
                    'from_keys[%s] %s contains *' % (
                        mapping_key, from_key))
   
    def _isValidFromValues(self):
        '''Check from values are valid.''' 
        for mapping_key, from_value in self.from_values.items():
            if not util.isInstanceOf(from_value, [str, unicode]):
                raise TypeError(
                    'from_values[%s] type is %s while '
                    'expected type is [str, unicode]: %s' % (
                        mapping_key, type(from_value), from_value))
            
            if '*' in from_value:
                raise KeyError(
                    'from_values[%s] %s contains *' % (
                        mapping_key, from_value))

    def _isValidOverrideConditions(self):
        '''Check override conditions are valid.'''
        override_items = self.override_conditions.items()
        for mapping_key, override_condition in override_items:
            if not util.isInstanceOf(override_condition, [str, unicode]):
                raise TypeError(
                    'override_conditions[%s] type is %s '
                    'while expected type is [str, unicode]: %s' % (
                        mapping_key, type(override_condition),
                        override_condition))

            if '*' in override_condition:
                raise KeyError(
                    'override_conditions[%s] %s contains *' % (
                        mapping_key, override_condition))

    def isValid(self):
        '''Check key translator is valid.'''
        self._isValidTranslatedKeys()
        self._isValidFromKeys()
        self._isValidFromValues()
        self._isValidOverrideConditions()    

    def getTranslatedKeys(self, ref_key, sub_ref):
        '''Get translated keys from ref_key and ref to ref_key.'''
        key_configs = {}
        for mapping_key, from_key in self.from_keys.items():
            if from_key in sub_ref:
                key_configs[mapping_key] = sub_ref[from_key]
            else:
                logging.error('from_key %s missing in %s',
                              from_key, sub_ref)

        translated_keys = []
        for translated_key in self.translated_keys:
            if callable(translated_key):
                try:
                    translated_key = translated_key(
                        sub_ref, ref_key, **key_configs)
                except Exception as error:
                    msg = '%s fails to get translated key by %s[%s](**%s)'
                    logging.error(msg, translated_key, ref_key, key_configs)
                    logging.exception(error)
                    continue

            if not translated_key:
                continue

            if not util.isInstanceOf(translated_key, [str, unicode]):
                logging.error('translated key %s should be [str, unicode]',
                              translated_key)
                continue

            translated_keys.append(translated_key)

        return translated_keys

    def getTranslatedValue(self, ref_key, sub_ref,
                           translated_key,  translated_sub_ref):
        '''
           Get translated value from ref_key, ref from ref_key,
           translated_key, translated_ref from translated_key.
        '''
        if self.translated_value is None:
            return sub_ref.config
        elif not callable(self.translated_value):
            return self.translated_value

        value_configs = {}
     
        for mapping_key, from_value in self.from_values.items():
            if from_value in sub_ref:
                value_configs[mapping_key] = sub_ref[from_value]
            else:
                logging.info('ignore from value %s for key %s',
                             from_value, ref_key)
          
        try:
            return self.translated_value(
                sub_ref, ref_key, translated_sub_ref,
                translated_key, **value_configs)
        except Exception as error:
            logging.error(
                '%s failed to get translated_value to %s by %s(**%s)',
                self, translated_key, ref_key, value_configs)
            logging.exception(error)
            return None

    def getOverride(self, ref_key, sub_ref,
                    translated_key, translated_sub_ref):
        '''
           Get override from ref_key, ref from ref_key,
           translated_key, translated_ref from translated_key.
        '''
        if not callable(self.override):
            return self.override

        override_condition_configs = {}
        override_items = self.override_conditions.items()
        for mapping_key, override_condition in override_items:
            if override_condition in sub_ref:
                override_condition_configs[mapping_key] = \
                    sub_ref[override_condition]
            else:
                logging.info('no override condition %s in %s',
                             override_condition, ref_key)

        try:
            return self.override(sub_ref, ref_key,
                                 translated_sub_ref,
                                 translated_key,
                                 **override_condition_configs)
        except Exception as error:
            msg = '%s failed to get override by (%s, %s, **%s)'
            logging.error(msg, self.override, ref_key,
                          translated_key,
                          override_condition_configs)
            logging.exception(error)
            return False
   
    def translate(self, ref, key, translated_ref):
        '''translate content in ref[key] to translated_ref.''' 
        for ref_key, sub_ref in ref.refItems(key):
            translated_keys = self.getTranslatedKeys(ref_key, sub_ref)
            for translated_key in translated_keys:
                translated_sub_ref = translated_ref.setdefault(
                    translated_key)
                translated_value = self.getTranslatedValue(
                    ref_key, sub_ref, translated_key, translated_sub_ref)

                if translated_value is None:
                    continue
                
                override = self.getOverride(
                    ref_key, sub_ref, translated_key, translated_sub_ref)
                translated_sub_ref.update(translated_value, override)


class ConfigTranslator(object):
    '''
        Class to translate origin config to expected dest config.

    Example:
        config = {
            'networking': {
                'management': {
                    'ip': '1.2.3.4',
                    'nic': 'eth0',
                },
                'public': {
                    'ip': '2.3.4.5',
                    'nic': 'eth0',
                },
            },
            'security': {
                'user': 'root',
                'password': 'root',
            },
        }
        translator = ConfigTranslator(
            '/networking/*/ip': [KeyTranslator(
                translated_keys=[
                    functools.partial(
                        config_translator_callbacks.getKeyFromPattern,
                        to_pattern='/modify_interface/ipaddress-%(nic)s'),
                    ),
                ],
                from_keys={'nic': '../nic'},
                override=functools.partial(
                    config_translator_callbacks.overridePathHas,
                    should_exist='management')
            )],
            '/networking/*/nic': [KeyTranslator(
                translated_keys=[functools.partial(
                    config_translator_callbacks.getKeyFromPattern,
                    to_pattern='/modify_interface/static-%(nic)s')],
                from_keys={'nic': '../nic'},
                translated_value=True,
                override=functools.partial(
                    config_translator_callbacks.overridePathHas,
                    should_exist='management'),
            )],
            '/security/user': [KeyTranslator(
                translated_keys=['/ksmeta/username'] 
            )],
        translated_config = translator.translate(config)
        translated_config == {
            'modify_interface': {
                'ipaddress-eth0': '1.2.3.4',
                'static-eth0': True 
            },
            'ksmeta': {
                'username': 'root',
            },
        }
    '''

    def __init__(self, mapping):
        self.mapping = mapping
        self.isValid()

    def isValid(self):
        '''Check if COnfigTranslator is valid.'''
        if not isinstance(self.mapping, dict):
            raise TypeError(
                'mapping type is %s while expected type is dict: %s' % (
                    type(self.mapping), self.mapping))

        for key, values in self.mapping.items():
            if not isinstance(values, list):
                msg = 'mapping[%s] type is %s while expected type is list: %s'
                raise TypeError(msg % (key, type(values), values))
            for i, value in enumerate(values):
                if not isinstance(value, KeyTranslator):
                    msg = (
                        'mapping[%s][%d] type is %s '
                        'while expected type is KeyTranslator: %s')
                    raise TypeError(msg % (key, i, type(value), value))

    def translate(self, config):
        '''translate config.

        Args:
            config: any type of data.

        Returns:
            the translated config.
        '''
        ref = config_reference.ConfigReference(config)
        translated_ref = config_reference.ConfigReference({})
        for key, values in self.mapping.items():
            for value in values:
                value.translate(ref, key, translated_ref)
        
        translated_config = config_reference.getCleanConfig(
            translated_ref.config)
        logging.debug('translate config\n%s\nto\n%s',
                      config, translated_config)
        return translated_config
