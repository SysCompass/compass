'''callback lib for config translator callbacks.'''
import crypt
import logging
import re

from compass.utils import util


def getKeyFromPattern(
    _ref, path, from_pattern='.*',
    to_pattern='', **kwargs):
    '''Get translated key from pattern'''
    match = re.match(from_pattern, path)
    if not match:
        return None
    group = match.groupdict()
    util.mergeDict(group, kwargs)
    try:
        translated_key = to_pattern % group
    except Exception as error:
        logging.error('failed to get translated key from %s %% %s',
                      to_pattern, group)
        logging.exception(error)
        return None
    return translated_key


def getEncryptedValue(ref, _path, _translated_ref, _translated_path,
                      crypt_method=None, **_kwargs):
    '''Get encrypted value.'''
    if not crypt_method:
        crypt_method = crypt.METHOD_MD5
    return crypt.crypt(ref.config, crypt_method)


def getValueIf(ref, _path, _translated_ref, _translated_path,
               condition=False, **_kwargs):
    '''Get value if condition is true.'''
    if not condition:
        return None
    return ref.config


def addValue(ref, path, translated_ref,
             translated_path, condition='', **_kwargs):
    '''Append value into translated config if condition.''' 
    logging.debug('add value %s from %s to %s if %s',
                  ref.config, path, translated_path, condition)
    if not translated_ref.config:
        value_list = []
    else:
        value_list = [
            value for value in translated_ref.config.split(',') if value
        ]

    if condition and ref.config not in value_list:
        value_list.append(ref.config)

    return ','.join(value_list)


def overrideIfAny(_ref, _path, _translated_ref, _translated_path, **kwargs):
    '''override if any kwargs is True'''
    return any(kwargs.values())


def overrideIfAll(_ref, _path, _translated_ref, _translated_path, **kwargs):
    '''override if all kwargs are True'''
    return all(kwargs.values())


def overridePathHas(_ref, path, _translated_ref, _translated_path,
                    should_exist='', **_kwargs):
    '''override if expect part exists in path.'''
    return should_exist in path.split('/')
