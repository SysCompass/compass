'''ConfigMerger Callbacks module.'''
import itertools
import logging
from copy import deepcopy
from netaddr import IPSet, IPRange

from compass.utils import util


def _getRoleBundleMapping(roles, bundles):
    '''Get role bundles.

    Args:
        roles: list of string.
        bundles: list of lsit of str.

    Returns:
        bundle_mapping: dict of {str: str}, mapping from role to
                        its bundled role.
        role_bundles: dict of {str: set of str}, mapping
                      bundled role to the roles bundled to it.
    '''
    bundle_mapping = {}
    for role in roles:
        bundle_mapping[role] = role

    for bundle in bundles:
        bundled_role = None
        for role in bundle:
            if role not in roles:
                continue
            while role != bundle_mapping[role]:
                role = bundle_mapping[role]
            if not bundled_role:
                bundled_role = role
            else:
                bundle_mapping[role] = bundled_role

    role_bundles = {}
    for role in roles:
        bundled_role = role
        while bundled_role != bundle_mapping[bundled_role]:
            bundled_role = bundle_mapping[bundled_role]
        bundle_mapping[role] = bundled_role
        role_bundles.setdefault(bundled_role, set()).add(role)

    logging.debug('bundle_mapping is %s', bundle_mapping)
    logging.debug('role_bundles is %s', role_bundles)
    return bundle_mapping, role_bundles


def _getBundledExclusives(exclusives, bundle_mapping):
    '''Get bundled exclusives.'''
    bundled_exclusives = set()
    for exclusive in exclusives:
        if exclusive not in bundle_mapping:
            logging.error(
                'exclusive role %s did not found in roles %s',
                exclusive, bundle_mapping.keys())
            continue
        bundled_exclusives.add(bundle_mapping[exclusive])

    logging.debug('bundled exclusives: %s', bundled_exclusives)
    return bundled_exclusives


def _getBundledMaxMins(maxs, mins, default_max, default_min, role_bundles):
    '''Get max and mins for each bundled role.'''
    bundled_maxs = {}
    bundled_mins = {}
    default_min = max(default_min, 0)
    if default_max < 0:
        default_max = default_max
    else:
        default_max = max(default_max, default_min)

    for bundled_role, roles in role_bundles.items():
        bundled_min = None
        bundled_max = None
        for role in roles:
            new_max = maxs.get(role, default_max)
            new_min = mins.get(role, default_min)
            if bundled_min is None:
                bundled_min = new_min
            else:
                bundled_min = min(bundled_min, max(new_min, 0))

            if bundled_max is None:
                bundled_max = new_max
            elif bundled_max < 0:
                if new_max >= 0:
                    bundled_max = max(new_max, bundled_min)
                else:
                    bundled_max = new_max
            elif new_max >= 0:
                bundled_max = max(min(bundled_max, new_max), bundled_min)
            else:
                bundled_max = max(bundled_max, bundled_min)

        if bundled_min is None:
            bundled_min = default_min

        if bundled_max is None:
            bundled_max = max(default_max, bundled_min)

        bundled_mins[bundled_role] = bundled_min
        bundled_maxs[bundled_role] = bundled_max

    logging.debug('bundled_maxs are %s', bundled_maxs)
    logging.debug('bundled_mins are %s', bundled_mins)
    return bundled_maxs, bundled_mins


def _updateAssignedRoles(lower_refs, to_key, bundle_mapping,
                         role_bundles, bundled_maxs, bundled_mins):
    '''
       update bundled maxs/mins and get assign roles to each
       host, unassigned host.
    '''
    lower_roles = {}
    unassigned_hosts = []
    for lower_key, lower_ref in lower_refs.items():
        roles_per_host = lower_ref.get(to_key, [])
        roles = set()
        bundled_roles = set()
        for role in roles_per_host:
            if role in bundle_mapping:
                bundled_role = bundle_mapping[role]
                bundled_roles.add(bundled_role)
                roles |= set(role_bundles[bundled_role])
        for bundled_role in bundled_roles:
            bundled_maxs[bundled_role] -= 1
            bundled_mins[bundled_role] -= 1
        lower_roles[lower_key] = list(roles)
        if not roles:
            unassigned_hosts.append(lower_key)

    logging.debug('assigned roles: %s', lower_roles)
    logging.debug('unassigned_hosts: %s', unassigned_hosts)
    logging.debug('bundled maxs for unassigned hosts: %s', bundled_maxs)
    logging.debug('bundled mins for unassigned hosts: %s', bundled_mins)
    return lower_roles, unassigned_hosts


def _updateExclusiveRoles(bundled_exclusives, lower_roles,
                          unassigned_hosts, bundled_maxs,
                          bundled_mins, role_bundles):
    '''Assign exclusive roles to hosts.'''
    for bundled_exclusive in bundled_exclusives:
        while bundled_mins[bundled_exclusive] > 0:
            if not unassigned_hosts:
                raise ValueError('no enough unassigned hosts for exlusive %s',
                                 bundled_exclusive)
            host = unassigned_hosts.pop(0)
            bundled_mins[bundled_exclusive] -= 1
            bundled_maxs[bundled_exclusive] -= 1
            lower_roles[host] = list(role_bundles[bundled_exclusive])
        del role_bundles[bundled_exclusive]

    logging.debug('assigned roles after assigning exclusives: %s', lower_roles)
    logging.debug('unassigned_hosts after assigning exclusives: %s',
                  unassigned_hosts)
    logging.debug('bundled maxs after assigning exclusives: %s', bundled_maxs)
    logging.debug('bundled mins after assigning exclusives: %s', bundled_mins)


def _assignRolesByMins(role_bundles, lower_roles, unassigned_hosts,
                       bundled_maxs, bundled_mins):
    '''Assign roles to hosts by min restriction.'''
    available_hosts = deepcopy(unassigned_hosts)
    for bundled_role, roles in role_bundles.items():
        while bundled_mins[bundled_role] > 0:
            if not available_hosts:
                raise ValueError('no enough available hosts to assign to %s',
                                 bundled_role)
            host = available_hosts.pop(0)
            available_hosts.append(host)
            if host in unassigned_hosts:
                unassigned_hosts.remove(host)
            bundled_mins[bundled_role] -= 1
            bundled_maxs[bundled_role] -= 1
            lower_roles[host] = list(roles)

    logging.debug('assigned roles after assigning mins: %s', lower_roles)
    logging.debug('unassigned_hosts after assigning mins: %s',
                  unassigned_hosts)
    logging.debug('bundled maxs after assigning mins: %s', bundled_maxs)


def _assignRolesByMaxs(role_bundles, lower_roles, unassigned_hosts,
                       bundled_maxs):
    '''Assign roles to host by max restriction.'''
    available_lists = []
    default_roles = []
    for bundled_role in role_bundles.keys():
        if bundled_maxs[bundled_role] > 0:
            available_lists.append(
                [bundled_role]*bundled_maxs[bundled_role])
        else:
            default_roles.append(bundled_role)
    available_list = util.getListWithPossibility(available_lists)

    for bundled_role in available_list:
        if not unassigned_hosts:
            break
        host = unassigned_hosts.pop(0)
        lower_roles[host] = list(role_bundles[bundled_role])

    logging.debug('assigned roles after assigning max: %s', lower_roles)
    logging.debug('unassigned_hosts after assigning maxs: %s',
                  unassigned_hosts)

    if default_roles:
        default_iter = itertools.cycle(default_roles)
        while unassigned_hosts:
            host = unassigned_hosts.pop(0)
            bundled_role = default_iter.next()
            lower_roles[host] = list(role_bundles[bundled_role])

    logging.debug('assigned roles are %s', lower_roles)
    logging.debug('unassigned hosts: %s', unassigned_hosts)


def assignRoles(_upper_ref, _from_key, lower_refs, to_key,
                roles=[], maxs={}, mins={}, default_max=-1,
                default_min=0, exclusives=[], bundles=[], **_kwargs):
    '''Assign roles to lower configs.'''
    logging.debug(
        'assignRoles with roles=%s, maxs=%s, mins=%s, '
        'default_max=%s, default_min=%s, exclusives=%s, bundles=%s',
        roles, maxs, mins, default_max,
        default_min, exclusives, bundles)
    bundle_mapping, role_bundles = _getRoleBundleMapping(roles, bundles)
    bundled_exclusives = _getBundledExclusives(exclusives, bundle_mapping)
    bundled_maxs, bundled_mins = _getBundledMaxMins(
        maxs, mins, default_max, default_min, role_bundles)

    lower_roles, unassigned_hosts = _updateAssignedRoles(
        lower_refs, to_key, bundle_mapping, role_bundles,
        bundled_maxs, bundled_mins)
    _updateExclusiveRoles(bundled_exclusives, lower_roles, unassigned_hosts,
                          bundled_maxs, bundled_mins, role_bundles)

    _assignRolesByMins(
        role_bundles, lower_roles, unassigned_hosts,
        bundled_maxs, bundled_mins)
    _assignRolesByMaxs(
        role_bundles, lower_roles, unassigned_hosts,
        bundled_maxs)
    
    return lower_roles


def assignRolesByHostNumbers(upper_ref, from_key, lower_refs, to_key,
                             policy_by_host_numbers={}, default={},
                             **_kwargs):
    '''assign roles by role assign policy.'''
    host_numbers = str(len(lower_refs))
    policy_kwargs = deepcopy(default)
    if host_numbers in policy_by_host_numbers:
        util.mergeDict(policy_kwargs, policy_by_host_numbers[host_numbers])

    return assignRoles(upper_ref, from_key, lower_refs,
                       to_key, **policy_kwargs)


def hasIntersection(upper_ref, from_key, _lower_refs, to_key,
                    lower_values={}, **_kwargs):
    '''Check if upper config has intersection with lower values.'''
    has_intersection = {}
    for lower_key, lower_value in lower_values.items():
        values = set(lower_value)
        intersection = values.intersection(set(upper_ref.config))
        logging.debug(
            'lower_key %s values %s intersection'
            'with from_key %s value %s: %s',
            lower_key, values, from_key, upper_ref.config, intersection)
        if intersection:
            has_intersection[lower_key] = True
        else:
            has_intersection[lower_key] = False

    logging.debug('assign %s: %s', to_key, has_intersection)
    return has_intersection


def assignIPs(_upper_ref, _from_key, lower_refs, to_key,
              ip_start='192.168.0.1', ip_end='192.168.0.254',
              **_kwargs):
    '''assign ips to hosts.'''
    if not ip_start or not ip_end:
        return {}
    host_ips = {}
    unassigned_hosts = []
    ips = IPSet(IPRange(ip_start, ip_end))
    for lower_key, lower_ref in lower_refs.items():
        ip_addr = lower_ref.get(to_key, '')
        if ip_addr:
            host_ips[lower_key] = ip_addr
            ips.remove(ip_addr)
        else:
            unassigned_hosts.append(lower_key)

    for ip_addr in ips:
        if not unassigned_hosts:
            break

        host = unassigned_hosts.pop(0)
        host_ips[host] = str(ip_addr)

    logging.debug('assign %s: %s', to_key, host_ips)
    return host_ips


def assignFromPattern(_upper_ref, from_key, lower_refs, to_key,
                      upper_keys=[], lower_keys=[], pattern='', **kwargs):
    '''assign to_key by pattern.'''
    host_values = {}
    upper_configs = {}
    for key in upper_keys:
        upper_configs[key] = kwargs.get(key, '')

    for lower_key, _ in lower_refs.items():
        group = deepcopy(upper_configs)
        for key in lower_keys:
            group[key] = kwargs.get(key, {}).get(lower_key, '')

        try: 
            host_values[lower_key] = pattern % group
        except Exception as error:
            logging.error('failed to assign %s[%s] = %s %% %s',
                          lower_key, to_key, pattern, group)
            logging.exception(error)

    logging.debug('assign %s from %s: %s', to_key, from_key, host_values)
    return host_values


def assignNoProxy(_upper_ref, _from_key, lower_refs,
                  to_key, default=[], hostnames={}, ips={},
                  **_kwargs):
    '''Assign no proxy to hosts.'''
    no_proxy_list = deepcopy(default)
    for _, hostname in hostnames.items():
        no_proxy_list.append(hostname)

    for _, ip_addr in ips.items():
        no_proxy_list.append(ip_addr)
    
    logging.debug('no_proxy_list: %s', no_proxy_list)
    no_proxy = ','.join(no_proxy_list)
    host_no_proxy = {}
    for lower_key, _ in lower_refs.items():
        host_no_proxy[lower_key] = no_proxy

    logging.debug('assign %s: %s', to_key, host_no_proxy)
    return host_no_proxy
