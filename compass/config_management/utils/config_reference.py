'''Config Reference module.
util to access the nested dict easily.
Example: To access the element config['network']['management']['ip'] in
         config = {'network': {'management': {'ip': '1.2.3.4'}}}
         ref = config_reference.ConfigReference(config)
         ref['/network/management/ip'] to access the item directly.
'''
import fnmatch
import os.path
from copy import deepcopy

from compass.utils import util


def getCleanConfig(config):
    """Get cleaned config from original config.

    Args:
        config: any type.

    Returns:
        any type. If some field in config is None or all items in the dict 
        is None recursively, does not include it in the cleaned config. 

    Example:
        config = {'network': {'management': {'ip': None}}}
        getCleanConfig(config) == None
    """
    if config is None:
        return None
    if isinstance(config, dict):
        extracted_config = {}
        for key, value in config.items():
            sub_config = getCleanConfig(value)
            if sub_config is not None:
                extracted_config[key] = sub_config
        if not extracted_config:
            return None
        return extracted_config
    else:
        return config


class ConfigReference(object):
    """Helper class to progress config which is deep nested dict."""

    def __init__(self, config, parent=None, parent_key=None):
        if parent and not isinstance(parent, self.__class__):
            raise TypeError('parent %s type should be %s'
                            % (parent, self.__class__.__name__))
        if parent_key and not util.isInstanceOf(parent_key, [str, unicode]):
            raise TypeError('parent_key %s type should be [str, unicode]'
                            % parent_key)
        self.config = config
        self._refs = {'.': self}
        self.parent = parent
        self.parent_key = parent_key
        if parent:
            self._refs['..'] = parent
            self._refs['/'] = parent._refs['/']
            parent._refs[parent_key] = self
            if parent.config is None or not isinstance(parent.config, dict):
                parent.__init__({}, parent=parent.parent,
                                parent_key=parent.parent_key)
            parent.config[parent_key] = config
        else:
            self._refs['..'] = self
            self._refs['/'] = self
        if config and isinstance(config, dict):
            for key, value in config.items():
                if not util.isInstanceOf(key, [str, unicode]):
                    msg = 'key type is %s while expected is [str, unicode]: %s'
                    raise TypeError(msg % (type(key), key))
                ConfigReference(value, self, key)

    def items(self, prefix=''):
        '''Return key value pair of all items.'''
        to_list = []
        for key, ref in self._refs.items():
            if not self.specialPath(key):
                key_prefix = os.path.join(prefix, key)
                to_list.append((key_prefix, ref.config))
                to_list.extend(ref.items(key_prefix))
        return to_list

    def keys(self):
        '''Return keys of all items.'''
        return [key for key, _ in self.items()]

    def values(self):
        '''Return values of all items.'''
        return [ref for _, ref in self.items()]

    def __iter__(self):
        return iter(self.keys())

    @classmethod
    def specialPath(cls, path):
        '''Check if path is special.'''
        return path in ['/', '.', '..']

    def refItems(self, path):
        '''Return the refs of the glob path.

        Args:
            path: str, glob pattern. like '/networking/*/ip',

        Returns:
            dict of {key: ConfigReference instance}.

        Example:
            config = {'network': {'management': {'ip': '1.2.3.4'},
                                  'public': {'ip': '2.3.4.5'}}}
            ref = ConfigReference(config)
            refs = ref.refItems('/networking/*/ip')
            refs['/networking/management/ip'].config = '1.2.3.4'
            refs['/networking/public/ip'].config = '2.3.4.5'
        '''
        if not path:
            raise KeyError('key %s is empty' % path)
        parts = []

        if util.isInstanceOf(path, [str, unicode]):
            parts = path.split('/')
        else:
            parts = path

        if not parts[0]:
            parts = parts[1:]
            refs = [('/', self._refs['/'])]
        else:
            refs = [('', self)]

        for part in parts:
            if not part:
                continue

            next_refs = []
            for prefix, ref in refs:
                if self.specialPath(part):
                    sub_prefix = os.path.join(prefix, part)
                    next_refs.append((sub_prefix, ref._refs[part]))
                    continue

                for sub_key, sub_ref in ref._refs.items():
                    if self.specialPath(sub_key):
                        continue

                    matched = fnmatch.fnmatch(sub_key, part)
                    if not matched:
                        continue

                    sub_prefix = os.path.join(prefix, sub_key)
                    next_refs.append((sub_prefix, sub_ref))

            refs = next_refs

        return refs

    def refKeys(self, path):
        '''Return keys of refitems.'''
        return [key for key, _ in self.refItems(path)]

    def refValues(self, path):
        '''Return values of refItems.'''
        return [ref for _, ref in self.refItems(path)]

    def ref(self, path, create_if_not_exist=False):
        '''Get ref of the path.

        Args:
           path: str. The path to the ref
           create_if_not_exists: bool, create ref if it
                                 does not exist on the path.
       
        Returns:
            ConfigReference instance to the position of the path.

        Exceptions:
            KeyError: if the path does not exist.
            TypeError: if the path is glob pattern.

        Examples:
            config = {'networking': {'management': {'ip': '1.2.3.4'}}}
            ref = ConfigReference(config)
            sub_ref = ref.ref('/networking/management/ip')
            sub_ref.config == '1.2.3.4'
 
            sub_ref = ref.ref('/networking/public/ip', True)
            ref.config = {'netwroking': {'management': {'ip': '1.2.3.4'},
                                         'public': {'ip': None}}
        ''' 
        if not path:
            raise KeyError('key %s is empty' % path)
        if '*' in path or '?' in path:
            raise TypeError('key %s should not contain *')
        parts = []
        if isinstance(path, list):
            parts = path
        else:
            parts = path.split('/')
        if not parts[0]:
            ref = self._refs['/']
            parts = parts[1:]
        else:
            ref = self
        for part in parts:
            if not part:
                continue
            if part in ref._refs:
                ref = ref._refs[part]
            elif create_if_not_exist:
                ref = ConfigReference(None, ref, part)
            else:
                raise KeyError('key %s is not exist' % path)
        return ref

    def __repr__(self):
        return '<ConfigReference: config=%r, refs[%s]>' % (self.config,
                                                           self._refs.keys())

    def __getitem__(self, path):
        return self.ref(path).config

    def __contains__(self, path):
        try:
            self.ref(path)
            return True
        except KeyError:
            return False

    def __setitem__(self, path, value):
        ref = self.ref(path, True)
        ref.__init__(value, ref.parent, ref.parent_key)
        return ref.config

    def __delitem__(self, path):
        ref = self.ref(path)
        if ref.parent:
            del ref.parent._refs[ref.parent_key]
            del ref.parent.config[ref.parent_key]
        ref.__init__(None)

    def update(self, config, override=True):
        '''Update ConfigReference instance with config.

        Args:
            config: any type
            override: bool, if the instance config should be overrided.

        Returns:
            None

        Examples:
            config = {'networking': {'management': {'ip': '1.2.3.4'}}}
            ref = ConfigReference(config)
            new_config = {'networking': {
                'management': {'mac': '00:00:00:00:00:00', 'ip': '2.3.4.5'}
            }}
            ref.update(new_config)
            ref.config == {'networking': {
                'management': {'ip': '1.2.3.4', 'mac': '00:00:00:00:00:00'}
            }}
            ref.update(new_config, True)
            ref.config == {'networking': {
                'management': {'ip': '2.3.4.5', 'mac': '00:00:00:00:00:00'}
            }}
        '''    
        if (self.config is not None and
                isinstance(self.config, dict) and
                isinstance(config, dict)):

            util.mergeDict(self.config, config, override)
        elif self.config is None or override:
            self.config = deepcopy(config)
        else:
            return

        self.__init__(self.config, self.parent, self.parent_key)

    def get(self, path, default=None):
        '''
           get config of the path. If config doest not exist in path,
           return default.
        '''
        try:
            return self[path]
        except KeyError:
            return default

    def setdefault(self, path, value=None):
        '''
           if path exists, return ref to the path, otherwise,
           set value to the path and return ref to the path.
        '''
        ref = self.ref(path, True)
        if ref.config is None:
            ref.__init__(value, ref.parent, ref.parent_key)
        return ref
