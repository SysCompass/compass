'''Filter config based on allows and denies rules.

Example:
    config = {
        'networking': {
            'management': {'ip': '1.2.3.4', 'mac': '00:00:00:00:00'},
            'public': {'ip': '2.3.4.5'}
        },
        'security': {'username': '1234', 'password': '1234'},
    }
    filter = ConfigFilter(allows=['/networking/*'],
                          denies=['/networking/*/mac'])
    filtered_config = filtere.filter(config)
    filtered_config == {
        'networking': {
            'management': {'ip': '1.2.3.4'},
            'public': {'ip': '2.3.4.5'},
        },
    }
'''
import logging

from compass.config_management.utils import config_reference


class ConfigFilter(object):
    '''config filter'''
 
    def __init__(self, allows=['*'], denies=[]):
        self.allows = allows
        self.denies = denies
        self.isValid()

    def _isAllowsValid(self):
        '''Check if allows are valid'''
        if not isinstance(self.allows, list):
            raise TypeError(
                'allows type is %s but expected type is list: %s' % (
                    type(self.allows), self.allows))
        for i, allow in enumerate(self.allows):
            if not isinstance(allow, str):
                raise TypeError(
                    'allows[%s] type is %s but expected type is str: %s' % (
                        i, type(allow), allow))

    def _isDeniesValid(self):
        '''Check if denies are valid.'''
        if not isinstance(self.denies, list):
            raise TypeError(
                'denies type is %s but expected type is list: %s' % (
                    type(self.denies), self.denies))
        for i, deny in enumerate(self.denies):
            if not isinstance(deny, str):
                raise TypeError(
                    'denies[%s] type is %s but expected type is str: %s' % (
                        i, type(deny), deny))

    def isValid(self):
        '''Check if config filter is valid.'''
        self._isAllowsValid()
        self._isDeniesValid()

    def filter(self, config):
        '''Filter config'''
        ref = config_reference.ConfigReference(config)
        filtered_ref = config_reference.ConfigReference({})
        self._filterAllows(ref, filtered_ref)
        self._filterDenies(filtered_ref)
        filtered_config = config_reference.getCleanConfig(filtered_ref.config)
        logging.debug('filter config %s to %s', config, filtered_config)
        return filtered_config

    def _filterAllows(self, ref, filtered_ref):
        '''copy ref config with the allows to filtered ref.'''
        for allow in self.allows:
            if not allow:
                continue
            for sub_key, sub_ref in ref.refItems(allow):
                logging.log(
                    logging.DEBUG-2,
                    'allow %s by allow rule %s',
                    sub_key, allow)
                filtered_ref.setdefault(sub_key).update(sub_ref.config)

    def _filterDenies(self, filtered_ref):
        '''remove config from filter_ref by denies.'''
        for deny in self.denies:
            if not deny:
                continue
            for ref_key in filtered_ref.refKeys(deny):
                logging.log(
                    logging.DEBUG-2,
                    'deny %s by deny rule %s',
                    ref_key, deny)
                del filtered_ref[ref_key]
