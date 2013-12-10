'''util module'''
from copy import deepcopy


def mergeDict(lhs, rhs, override=True):
    '''merge right dict into left dict.
    Args:
        lhs: dict
        rhs: dict
        override: bool. the value in the right overides '
                  the value in left dict if True.

    Returns:
        None. lhs is updated by rhs.

    Exceptions:
        TypeError if lhs or rhs is not dict.
    '''
    if not rhs:
        return
    if not isinstance(lhs, dict):
        raise TypeError('lhs type is %s while expected is dict' % type(lhs),
                        lhs)
    if not isinstance(rhs, dict):
        raise TypeError('rhs type is %s while expected is dict' % type(rhs),
                        rhs)
    for key, value in rhs.items():
        if isinstance(value, dict) and\
           key in lhs and\
           isinstance(lhs[key], dict):
            mergeDict(lhs[key], value, override)
        else:
            if override or key not in lhs:
                lhs[key] = deepcopy(value)


def orderKeys(keys, orders):
    '''Get ordered keys.

    Args:
        keys: list
        orders: list, may contains '.' which means all other keys not
    appeared in orders.

    Returns:
        list sorted by orders

    Exceptions:
        TypeError if keys or orders is not list.
    '''
    if not isinstance(keys, list):
        raise TypeError('keys %s type should be list' % keys)
    if not isinstance(orders, list):
        raise TypeError('orders ^s type should be list' % orders)
    found_dot = False
    pres = []
    posts = []
    for order in orders:
        if order == '.':
            found_dot = True
        else:
            if found_dot:
                posts.append(order)
            else:
                pres.append(order)
    return [pre for pre in pres if pre in keys] +\
        [key for key in keys if key not in orders] +\
        [post for post in posts if post in keys]


def isInstanceOf(instance, expected_types):
    '''Check instance type is in one of expected types.

    Args:
        instance: object.
        expected_types: list of type. 

    Returns:
        True if instance type is of one of expect_types.
        Otherwise False.
    '''
    for expected_type in expected_types:
        if isinstance(instance, expected_type):
            return True
    return False


def getListWithPossibility(lists):
    '''Return list of item from list of list of identity item.

    Args:
        lists: list of list of identity item.

    Returns:
        list where for each first k elements, it should be the k most
        possible items. 

    Example:
        lists: ['a', 'a', 'a', 'a'], ['b', 'b'], ['c'],
        the expected output is ['a', 'b', 'c', 'a', 'a', 'b', 'a']
    '''
    lists = deepcopy(lists)
    lists = sorted(lists, key=len, reverse=True)
    list_possibility = []
    max_index = 0
    total_elements = 0
    possibilities = []
    for items in lists:
        list_possibility.append(0.0)
        length = len(items)
        if length > 0:
            total_elements += length
            possibilities.append(1.0/length)
        else:
            possibilities.append(0.0)
    output = []
    while total_elements > 0:
        if not lists[max_index]:
            list_possibility[max_index] -= total_elements
        else:
            list_possibility[max_index] -= possibilities[max_index]
            element = lists[max_index].pop(0)
            output.append(element)
            total_elements -= 1
        max_index = list_possibility.index(max(list_possibility))
    return output
