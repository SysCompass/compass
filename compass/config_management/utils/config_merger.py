'''Module to set the hosts configs from cluster config.'''
import logging
from copy import deepcopy

from compass.config_management.utils import config_reference
from compass.utils import util


class ConfigMapping(object):
    '''
       Class to merger config referred to path list in upper ref '
       to to_key in lower refs.
    
    Examples:
        upper_config = {
            'network': {
                'management': {
                    'ip_start': '10.145.88.100',
                    'ip_end': '10.145.88.255',
                    'netmask': '255.255.255.0',
                },
                'public': {
                    'ip_start': '192.168.100.100',
                    'ip_end': '192.168.200.255',
                },
            },
        }
        lower_configs = {
            1: {
                'network': {
                    'management': {
                        'ip': '10.145.88.150',
                    },
                },
            },
            2: {
                'network': {
                    'management': {
                        'ip': '10.145.88.151',
                    },
                },
            },
        }

        upper_ref = ConfigReference(upper_config)
        lower_refs = {}
        for lower_key, lower_config in lower_configs.items():
            lower_refs[lower_key] = ConfigReference(lower_config)

        mapper = ConfigMapper(
            path_list=['/network/*']
            from_upper_keys={'ip_start': 'ip_start', 'ip_end': 'ip_end'},
            to_key='ip',
            value=config_merger_callbacks.assignIPs
        )
        mapper.merge(upper_ref, lower_refs)
        lower_refs[0].config == {
            'network': {
                'management': {
                    'ip': 10.145.88.150',
                },
                'public': {
                    'ip': '192.168.100.100',
                },
            },
        }
        lower_refs[1].config == {
            'network': {
                'management': {
                    'ip': 10.145.88.151',
                },
                'public': {
                    'ip': '192.168.100.101',
                },
            },
        }
        mapper = ConfigMapper(
            path_list=['/network/*/netmask']
        )
        mapper.merge(upper_ref, lower_refs)
        lower_refs[0].config == {
            'network': {
                'management': {
                    'ip': 10.145.88.150',
                    'netmask': '255.255.255.0'
                },
                'public': {
                    'ip': '192.168.100.100',
                },
            },
        }
        lower_refs[1].config == {
            'network': {
                'management': {
                    'ip': 10.145.88.151',
                    'netmask': '255.255.255.0',
                },
                'public': {
                    'ip': '192.168.100.101',
                },
            },
        }
    '''

    def __init__(self, path_list, from_upper_keys={},
                 from_lower_keys={}, to_key='.', value=None):
        self.path_list = path_list
        self.from_upper_keys = from_upper_keys
        self.from_lower_keys = from_lower_keys
        self.to_key = to_key
        self.value = value

    def __str__(self):
        return (
            '%s[path_list:%s, from_upper_keys:%s, '
            'from_lower_keys: %s, to_key:%s, value:%s]'
        ) % (
            self.__class__.__name__,
            self.path_list, self.from_upper_keys,
            self.from_lower_keys, self.to_key,
            self.value)

    def _isValidPathList(self):
        '''Check path_list are valid.'''
        for i, path in enumerate(self.path_list):
            if not isinstance(path, str):
                raise TypeError(
                    'path_list[%d] type is %s while '
                    'expected type is str: %s' % (
                        i, type(path), path))

    def _isValidFromUpperKeys(self):
        '''Check from_upper_keys are valid.'''
        for mapping_key, from_upper_key in self.from_upper_keys.items():
            if not isinstance(from_upper_key, str):
                raise TypeError(
                    'from_upper_keys[%s] type is %s'
                    'while expected type is str: %s' % (
                        mapping_key, type(from_upper_key), from_upper_key))
            
            if '*' in from_upper_key:
                raise KeyError(
                    'from_upper_keys[%s] %s contains *' % (
                        mapping_key, from_upper_key))

    def _isValidFromLowerKeys(self):
        '''Check from_lower_keys are valid.'''
        for mapping_key, from_lower_key in self.from_lower_keys.items():
            if not isinstance(from_lower_key, str):
                raise TypeError(
                    'from_lower_keys[%s] type'
                    'is %s while expected type is str: %s' % (
                        mapping_key, type(from_lower_key), from_lower_key))

            if '*' in from_lower_key:
                raise KeyError(
                    'from_lower_keys[%s] %s contains *' % (
                        mapping_key, from_lower_key))

    def _isValidFromKeys(self):
        '''Check from keys are valid.'''
        self._isValidFromUpperKeys()
        self._isValidFromLowerKeys()
        upper_keys = set(self.from_upper_keys.keys())
        lower_keys = set(self.from_lower_keys.keys())
        intersection = upper_keys.intersection(lower_keys)
        if intersection:
            raise KeyError(
                'there is intersection between from_upper_keys %s'
                ' and from_lower_keys %s: %s' % (
                    upper_keys, lower_keys, intersection))
        
    def _isValidToKey(self):
        '''Check to_key is valid.'''
        if '*' in self.to_key:
            raise KeyError('to_key %s contains *' % self.to_key)
       
    def isValid(self):
        '''Check ConfigMapping instance is valid.'''
        self._isValidPathList()
        self._isValidFromKeys()
        self._isValidToKey()

    def _getUpperSubRefs(self, upper_ref):
        '''get sub_refs from upper_ref.''' 
        upper_refs = []
        for path in self.path_list:
            upper_refs.extend(upper_ref.refItems(path))
        return upper_refs

    def _getMappingFromUpperKeys(self, ref_key, sub_ref):
        '''Get upper config mapping from from_upper_keys.'''
        sub_configs = {}
        for mapping_key, from_upper_key in self.from_upper_keys.items():
            if from_upper_key in sub_ref:
                sub_configs[mapping_key] = sub_ref[from_upper_key]
            else:
                logging.info('ignore from_upper_key %s in %s',
                             from_upper_key, ref_key)
        return sub_configs

    def _getMappingFromLowerKeys(self, ref_key, lower_sub_refs):
        '''Get lower config mapping from from_lower_keys.'''
        sub_configs = {}
        for mapping_key, from_lower_key in self.from_lower_keys.items():
            sub_configs[mapping_key] = {}
            
        for lower_key, lower_sub_ref in lower_sub_refs.items():
            for mapping_key, from_lower_key in self.from_lower_keys.items():
                if from_lower_key in lower_sub_ref:
                    sub_configs[mapping_key][lower_key] = (
                        lower_sub_ref[from_lower_key])
                else:
                    msg = 'ignore from_lower_key %s in %s lower_key %s'
                    logging.error(msg, from_lower_key, ref_key, lower_key)
        return sub_configs 

    def _getValues(self, ref_key, sub_ref, lower_sub_refs, sub_configs):
        '''Get values to set to lower configs.'''
        if self.value is None:
            lower_values = {}
            for lower_key in lower_sub_refs.keys():
                lower_values[lower_key] = deepcopy(sub_ref.config)

            return lower_values
        elif not callable(self.value):
            lower_values = {}
            for lower_key in lower_sub_refs.keys():
                lower_values[lower_key] = deepcopy(self.value)

            return lower_values

        try:
            return self.value(sub_ref, ref_key, lower_sub_refs,
                              self.to_key, **sub_configs)
        except Exception as error:
            logging.error(
                '%s fails to get values from (%s, %s, %s, **%s)',
                self, ref_key, sub_ref, lower_sub_refs, sub_configs)
            logging.exception(error)
            return {}

    def merge(self, upper_ref, lower_refs):
        '''merge upper config to lower configs.'''
        upper_sub_refs = self._getUpperSubRefs(upper_ref)

        for ref_key, sub_ref in upper_sub_refs:
            sub_configs = self._getMappingFromUpperKeys(ref_key, sub_ref)

            lower_sub_refs = {}
            for lower_key, lower_ref in lower_refs.items():
                lower_sub_refs[lower_key] = lower_ref.setdefault(ref_key)

            lower_sub_configs = self._getMappingFromLowerKeys(
                ref_key, lower_sub_refs)

            util.mergeDict(sub_configs, lower_sub_configs)

            values  = self._getValues(
                ref_key, sub_ref, lower_sub_refs, sub_configs)

            logging.debug('%s set values %s to %s',
                          ref_key,  self.to_key, values)
            for lower_key, lower_sub_ref in lower_sub_refs.items():
                if lower_key not in values:
                    logging.error('no key %s in %s', lower_key, values)
                    continue
                value = values[lower_key]
                lower_sub_ref.setdefault(self.to_key, value)


class ConfigMerger(object):
    '''Class to merge upper config to lower configs.
 
    Examples:
        upper_config = {
            'network': {
                'management': {
                    'ip_start': '10.145.88.100',
                    'ip_end': '10.145.88.255',
                    'netmask': '255.255.255.0',
                },
                'public': {
                    'ip_start': '192.168.100.100',
                    'ip_end': '192.168.200.255',
                },
            },
        }
        lower_configs = {
            1: {
                'network': {
                    'management': {
                        'ip': '10.145.88.150',
                    },
                },
            },
            2: {
                'network': {
                    'management': {
                        'ip': '10.145.88.151',
                    },
                },
            },
        }

        merger = ConfigMerger(
            mappings=[ConfigMapper(
                path_list=['/network/*']
                from_upper_keys={'ip_start': 'ip_start', 'ip_end': 'ip_end'},
                to_key='ip',
                value=config_merger_callbacks.assignIPs
            ), ConfigMapper(
                path_list=['/network/*/netmask']
            )]
        merger.merge(upper_config, lower_configs)
        lower_configs == {
            1: {
                'network': {
                    'management': {
                        'ip': 10.145.88.150',
                        'netmask': '255.255.255.0'
                    },
                    'public': {
                        'ip': '192.168.100.100',
                    },
                },
            },
            2: {
                'network': {
                    'management': {
                        'ip': 10.145.88.151',
                        'netmask': '255.255.255.0',
                    },
                    'public': {
                        'ip': '192.168.100.101',
                    },
                },
            },
        }
    '''

    def __init__(self, mappings):
        self.mappings = mappings
        self.isValid()

    def isValid(self):
        '''Check ConfigMerger instance is valid.'''
        for mapping in self.mappings:
            if not mapping.isValid():
                return False
        return True

    def merge(self, upper_config, lower_configs):
        '''merge upper config to lower configs.

        Args:
            upper_config: any type.
            lower_configs: dict of {str: any type}

        Returns:
            None
        '''
        upper_ref = config_reference.ConfigReference(upper_config)
        lower_refs = {}
        for lower_key, lower_config in lower_configs.items():
            lower_refs[lower_key] = config_reference.ConfigReference(
                lower_config)

        for mapping in self.mappings:
            logging.debug('apply merging from the rule %s', mapping)
            mapping.merge(upper_ref, lower_refs)

        for lower_key, lower_config in lower_configs.items():
            lower_configs[lower_key] = config_reference.getCleanConfig(
                lower_config)

        logging.debug('merged upper config\n%s\nto lower configs:\n%s',
                      upper_config, lower_configs)
