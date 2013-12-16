'''compass api client library.'''
import logging
import json
import requests


class Client(object):
    '''wrapper for compass restful api.'''

    def __init__(self, url, auth=None, cert=None, cookies=None,
                headers=None, proxies=None, stream=None):
        self.url = url
        self.session = requests.Session()
        if auth:
            self.session.auth = auth

        if cert:
            self.session.cert = cert

        if cookies:
            self.session.cookies = cookies

        if headers:
            self.session.headers = headers

        if proxies is not None:
            self.session.proxies = proxies

        if stream is not None:
            self.session.stream = stream

    def __del__(self):
        self.session.close()

    @classmethod
    def get_response(cls, resp):
        '''decapsulate the resp to status code and python formatted data.'''
        resp_obj = {}
        try:
            resp_obj = resp.json()
        except Exception as error:
            logging.error('failed to load object from %s: %s',
                          resp.url, resp.content)
            logging.exception(error)
            resp_obj['status'] = 'Json Parsing Failure'
            resp_obj['message'] = resp.content

        return resp.status_code, resp_obj

    def get(self, relative_url, params=None):
        '''encapsulate get method.'''
        url = '%s%s' % (self.url, relative_url)
        if params:
            resp = self.session.get(url, params=params)
        else:
            resp = self.session.get(url)

        return self.get_response(resp)

    def post(self, relative_url, data=None):
        '''encapsulate post method.'''
        url = '%s%s' % (self.url, relative_url)
        if data:
            resp = self.session.post(url, json.dumps(data))
        else:
            resp = self.session.post(url)

        return self.get_response(resp)

    def put(self, relative_url, data=None):
        '''encapsulate put method.'''
        url = '%s%s' % (self.url, relative_url)
        if data:
            resp = self.session.put(url, json.dumps(data))
        else:
            resp = self.session.put(url)

        return self.get_response(resp)

    def delete(self, relative_url):
        '''encapsulate delete method.'''
        url = '%s%s' % (self.url, relative_url)
        return self.get_response(self.session.delete(url))

    def get_switches(self, switch_ips=None, switch_networks=None, limit=None):
        '''
           Get the details of switches filtered by switch_ips,
           switch_networks. The returned switches is limited by limit.

        Args:
            switch_ips: list of str. Each is as 'xxx.xxx.xxx.xxx'.
                        Only the switch(es) with the IP(s) will be returned.
            switch_networks: list of str. Each is as 'xxx.xxx.xxx.xxx/xx'.
                             Only the switch(es) with the IP(s) will
                             be returned.
            limit: int, Only the switch(es) with the IP(s) will be returned.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200.
                    resp_obj = {
                        'status': 'OK',
                        'switches': [{
                            'id': 1,
                            'state': 'under_monitoring',
                        }]
                    }
            error: status_code = 400 (UserInvalidUsage)
                   resp_obj = {
                       'status': '...'
                       'message': '...'
                   }
        '''
        params = {}
        if switch_ips:
            params['switchIp'] = switch_ips

        if switch_networks:
            params['switchIpNetwork'] = switch_networks

        if limit:
            params['limit'] = limit
        return self.get('/api/switches', params=params)

    def get_switch(self, switch_id):
        '''Lists details for a specified switch

        Args:
            switch_id: int, switch id.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'switch': {
                            'id': 1,
                            'state': 'under_monitoring',
                        },
                    }
            error: status_code = 404 (ObjectDoesNotExist)
                   resp_obj = {
                       'status': '...',
                       'message': '...',
        '''
        return self.get('/api/switches/%s' % switch_id)

    def add_switch(self, switch_ip, version=None, community=None,
                   username=None, password=None):
        '''
           Create a switch by providing a switch IP address and associated
           credentials.  The POST action shall trigger switch polling. During
           the polling process, MAC address of the devices connected to the
           switch will be learned by SNMP or SSH.

        Args:
            switch_ip: str, The switch IP address.
            version: str, SNMP version when accessing the specified
                     switch by SNMP.
            community: SNMP community when accessing the specified
                       switch by SNMP.
            username: SSH username when accessing the specified
                      switch by SSH.
            password: SSH password when accessing the specified
                      switch by SSH.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 202 (ObjectDoesNotExist)
                    resp_obj = {
                        'status': 'accepted',
                        'switch': {
                            'id': 1,
                            'state': 'not_reached',
                        },
                    }
            error: status_code = 409 (ObjectDuplicateError) or
                   status_code = 400 (UserInvalidUsage)
                   resp_obj = {
                       'status': '...',
                       'message': '...',
                   }
        '''
        data = {}
        data['switch'] = {}
        data['switch']['ip'] = switch_ip
        data['switch']['credential'] = {}
        if version:
            data['switch']['credential']['version' ] = version

        if community:
            data['switch']['credential']['community'] = community

        if username:
            data['switch']['credential']['username'] = username

        if password:
            data['switch']['credential']['password'] = password

        return self.post('/api/switches', data=data)

    def update_switch(self, switch_id, ip_addr=None,
                      version=None, community=None,
                      username=None, password=None):
        '''
           Updates the credentials of a specified switch, triggering polling
           switch action once update is successful.

        Args:
            switch_id: int, switch id
            ip_addr: str, as 'xxx.xxx.xxx.xxx' format. The switch IP address.
            version: str, one in ['v1', 'v2c'].
                     SNMP version when accessing the specified switch by SNMP.
            community: str, generally 'public'.
                       SNMP community when accessing the specified switch
                       by SNMP.
            username: str, SSH username when accessing the specified
                      switch by SSH.
            password: str, SSH password when accessing the specified
                      switch by SSH.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 202
                    resp_obj = {
                        'status': 'accepted',
                        'switch': {
                            'state': 'not_reached',
                        },
                    }
            error: status_code = 404,
                   resp_obj = {
                       'status': '...'
                       'message': '...',
                   }
        '''
        data = {}
        data['switch'] = {}
        if ip_addr:
            data['switch']['ip'] = ip_addr

        data['switch']['credential'] = {}
        if version:
            data['switch']['credential']['version' ] = version

        if community:
            data['switch']['credential']['community'] = community

        if username:
            data['switch']['credential']['username'] = username

        if password:
            data['switch']['credential']['password'] = password

        return self.put('/api/switches/%s' % switch_id, data=data)

    def delete_switch(self, switch_id):
        '''Not implemented in api.'''
        return self.delete('api/switches/%s' % switch_id)

    def get_machines(self, switch_id=None, vlan_id=None,
                     port=None, limit=None):
        '''
           Queries and lists the details for the device(s)
           filtered by switch ID or a switch IP network, and returns
           a specified number of results as designated by limit.

        Args:
            switch_id: int, Device(s) connected to the switch with
                            this ID will be returned.
            vlan_id: int, Device(s) belonging to this Vlan ID
                     will be returned.
            port: int, Device(s) having this Port number will be
                       returned
            limit: int, Up to this number of results will be returned.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'machines': [{
                            'mac': '28:6e:d4:47:c8:6c',
                            'vlan': 1,
                            'id': 30,
                            'port': 1,
                            'switch_ip': '172.29.8.40'
                        }],
                     }
            error: status_code = 400 (UserInvalidUsage)
                   resp_obj = {
                       'status': '...',
                       'message': '...'
                   }
        '''
        params = {}
        if switch_id:
            params['switchId'] = switch_id

        if vlan_id:
            params['vlanId'] = vlan_id

        if port:
            params['port'] = port

        if limit:
            params['limit'] = limit

        return self.get('/api/machines', params=params)

    def get_machine(self, machine_id):
        '''Lists the details for a specified device.

        Args:
            machine_id: int, The Device with this ID will be return.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'machine': {
                            'mac': '28:6e:d4:47:c8:6c',
                            'vlan': 1,
                            'id': 30,
                            'port': 1,
                            'switch_ip': '172.29.8.40'
                        }
                    }
            error: status_code = 404 (ObjectDoesNotExist)
                   resp_obj = {
                       'status': '...',
                       'message': '...'
                   }
        '''
        return self.get('/api/machines/%s' % machine_id)

    def get_clusters(self):
        '''Lists the details for all the clusters

        Args:
            No args.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'clusters': [{
                            'id': 1,
                            'clusterName': 'cluster1',
                        }],
                    }
        '''
        return self.get('/api/clusters')

    def get_cluster(self, cluster_id):
        '''Lists the details of the specified cluster.

        Args:
            cluster_id: int, The unique identifier of the cluster.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'cluster': {
                            'id': 1,
                            'clusterName': 'cluster1',
                        },
                    }
            error: status_code = 404 (ObjectDoesNotExist)
                   resp_obj = {
                       'status': '...',
                       'message': '...'
                   }
        '''
        return self.get('/api/clusters/%s' % cluster_id)

    def add_cluster(self, cluster_name, adapter_id):
        '''Creates a cluster by user-specified name.

        Args:
            cluster_name: str, The unique name of the cluster
                          specified by the user.
            adapter_id: int, The unique identifier of adapter.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code  = 200
                    resp_obj = {
                        'status': 'OK',
                        'cluster': {
                            'id': 1,
                            'name': 'cluster1',
                        },
                    }
            error: status_code = 409 (ObjectDuplicateError)
                   resp_obj = {
                       'status': '...',
                       'mesage': '...',
                   }
        '''
        data = {}
        data['cluster'] = {}
        data['cluster']['name'] = cluster_name
        data['cluster']['adapter_id'] = adapter_id
        return self.post('/api/clusters', data=data)

    def add_hosts(self, cluster_id, machine_ids):
        '''add the specified machine(s) as the host(s) to the cluster.

        Args:
            cluster_id: int, The unique identifier of the cluster
            machine_ids: list of int, each is the id of one machine.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'clusterHosts': [{
                            'id': 1,
                            'machine_id': 1,
                        }],
                    }
            error: status_code = 400 (UserInvalidUsage),
                                 404 (ObjectDoesNotExist)
                                 409 (ObjectDuplicateError)
                   resp_obj = {
                       'status': '...',
                       'message': '...',
                   }
        '''
        data = {}
        data['addHosts'] = machine_ids
        return self.post('/api/clusters/%s/action' % cluster_id, data=data)

    def remove_hosts(self, cluster_id, host_ids):
        '''remove the specified machine(s) as the host(s) from the cluster.

        Args:
            cluster_id: int, The unique identifier of the cluster
            host_ids: list of int, each is the id of one host.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'clusterHosts': [{
                            'id': 1,
                            'machine_id': 1,
                        }],
                    }
            error: status_code = 400 (UserInvalidUsage),
                                 404 (ObjectDoesNotExist)
                                 409 (ObjectDuplicateError)
                   resp_obj = {
                       'status': '...',
                       'message': '...',
                   }
        '''
        data = {}
        data['removeHosts'] = host_ids
        return self.post('/api/clusters/%s/action' % cluster_id, data=data)

    def replace_hosts(self, cluster_id, machine_ids):
        '''replace the cluster hosts with the specified machine(s).

        Args:
            cluster_id: int, The unique identifier of the cluster
            machine_ids: list of int, each is the id of one machine.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'clusterHosts': [{
                            'id': 1,
                            'machine_id': 1,
                        }],
                    }
            error: status_code = 400 (UserInvalidUsage),
                                 404 (ObjectDoesNotExist)
                                 409 (ObjectDuplicateError)
                   resp_obj = {
                       'status': '...',
                       'message': '...',
                   }
        '''
        data = {}
        data['replaceAllHosts'] = machine_ids
        return self.post('/api/clusters/%s/action' % cluster_id, data=data)

    def deploy_hosts(self, cluster_id):
        '''deploy the cluster..

        Args:
            cluster_id: int, The unique identifier of the cluster

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'accepted',
                        'deployment': '/progress/cluster/1',
                    }
            error: status_code = 400 (UserInvalidUsage),
                                 404 (ObjectDoesNotExist)
                                 409 (ObjectDuplicateError)
                   resp_obj = {
                       'status': '...',
                       'message': '...',
                   }
        '''
        data = {}
        data['deploy'] = {}
        return self.post('/api/clusters/%s/action' % cluster_id, data=data)

    @classmethod
    def parse_security(cls, kwargs):
        '''parse the arguments to security data.'''
        data = {}
        for key, value in kwargs.items():
            if key.endswith('_username'):
                key_name = key[:-len('_username')]
                data.setdefault(
                    '%s_credentials' % key_name, {})['username'] = value
            elif key.endswith('_password'):
                key_name = key[:-len('_password')]
                data.setdefault(
                    '%s_credentials' % key_name, {})['password'] = value

        return data

    def set_security(self, cluster_id, **kwargs):
        '''Update the cluster security configuration.

        Args:
            cluster_id: int, cluster id.
            <security_name>_username: str, username of the security name.
            <security_name>_password: str, passowrd of the security name.

            security_name should be one of ['server', 'service', 'console'].

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code  = 200
                    resp_obj = {
                        'status': 'OK',
                    }
            error: status_code = 400 (UserInvalidUsage, InputMissingError),
                                 404 (ObjectDoesNotExist)
                   resp_obj = {
                       'status': '...',
                       'message': '...'
                   }
        '''
        data = {}
        data['security'] = self.parse_security(kwargs)
        return self.put('/api/clusters/%s/security' % cluster_id, data=data)

    @classmethod
    def parse_networks(cls, kwargs):
        '''parse arguments to network data.'''
        data = {}
        for key, value in kwargs.items():
            if key.endswith('_interface'):
                key_name = key[:-len('_interface')]
                data[key_name] = value

        return data

    def set_networking(self, cluster_id,
                       global_setting, **kwargs):
        '''Update the cluster network configuration.

        Args:
            cluster_id: int, cluster id.
            global_setting: dict, global network setting.
                            the key should be:
                            'nameservers': str, comma seperated
                                           nameserver ip addr.
                            'search_path': str, dns name search path.
                            'gateway': str, gateway ip addr.
                            'proxy': str, optional. proxy url.
                            'ntp_server': str, optional, ip addr of
                                          ntp server.
            <interface_name>_intereface: dict, interface setting
                                         for interface_name.
                                         the interface name should be in:
                                         ['management', 'tenant', 'public',
                                          'storage']
                                         the key should be:
                                         'ip_start': str, start ip addr.
                                         'ip_end': str, end ip addr.
                                         'netmask': str, net mask of the
                                                    interface.
                                         'nic': str, physical if name.
                                         'promisc': 0 or 1. if the physical
                                                    if in promiscous mode.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code  = 200
                    resp_obj = {
                        'status': 'OK',
                    }
            error: status_code = 400 (UserInvalidUsage, InputMissingError),
                                 404 (ObjectDoesNotExist)
                   resp_obj = {
                       'status': '...',
                       'message': '...'
                   }
        '''
        data = {}
        data['networking'] = {}
        data['networking']['global'] = global_setting
        data['networking']['interfaces'] = self.parse_networks(kwargs)
        return self.put('/api/clusters/%s/networking' % cluster_id, data=data)

    @classmethod
    def parse_partition(cls, kwargs):
        '''parse arguments to partition data.'''
        data = {}
        for key, value in kwargs.items():
            if key.endswith('_partition_percentage'):
                key_name = key[:-len('_partition_percentage')]
                data[key_name] = '%s%%' % value
            elif key.endswitch('_partition_mbytes'):
                key_name = key[:-len('_partition_mbytes')]
                data[key_name] = str(value)

        partition = ';'.join([
            '/%s %s' % (key, value) for key, value in data.items()
        ])
        return partition

    def set_partition(self, cluster_id, **kwargs):
        '''Update the cluster partition configuration.

        Args:
            cluster_id: int, cluster id.
            <partition_name>_partition_percentage: float between 0 to 100.
                                                   percentage the partiton in
                                                   the total volume.
            <partition_name>_partition_mbytes: int, mbytes in partition.
            partition_name should be ['home', 'var', 'tmp']

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code  = 200
                    resp_obj = {
                        'status': 'OK',
                    }
            error: status_code = 400 (UserInvalidUsage, InputMissingError),
                                 404 (ObjectDoesNotExist)
                   resp_obj = {
                       'status': '...',
                       'message': '...'
                   }
        '''
        data = {}
        data['partition'] = self.parse_partition(kwargs)
        return self.put('/api/clusters/%s/partition' % cluster_id, data=data)

    def get_hosts(self, hostname=None, clustername=None):
        '''
           Queries and lists the details for all hosts or the host(s)
           specified by hostname and(or) clustername.

        Args:
            hostname: str, The name of a host.
            clustername: str, The name of a cluster.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'cluster_hosts': [{
                            'id': 1,
                            'hostname': 'host1',
                            'mutable': true,
                        ]},
                    }
        '''
        params = {}
        if hostname:
            params['hostname'] = hostname

        if clustername:
            params['clustername'] = clustername

        return self.get('/api/clusterhosts', params=params)

    def get_host(self, host_id):
        '''Lists the details for the specified host.

        Args:
            No args.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'cluster_host': {
                            'id': 1,
                            'hostname': 'host1',
                            'mutable': true,
                        },
                    }
            error: status_code = 404 (ObjectDoesNotExist)
                   resp_obj = {
                       'satus': '...',
                       'message': '...',
                   }
        '''
        return self.get('/api/clusterhosts/%s' % host_id)

    def get_host_config(self, host_id):
        '''Lists the details of the config for the specified host.

        Args:
            host_id: int, host id.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'config': {
                            'hostid': 1,
                            'hostname': 'host1',
                            'networking': {...},
                            'security': {...},
                            'partition': {...},
                            'roles': [...],
                        },
                    }
            error: status_code = 404 (ObjectDoesNotExist)
                   resp_obj = {
                       'satus': '...',
                       'message': '...',
                   }
        '''
        return self.get('/api/clusterhosts/%s/config' % host_id)

    def update_host_config(self, host_id, hostname=None,
                           networking_global_setting=None,
                           roles=None, **kwargs):
        '''
           Updates one or more editable attributes in config for
           the specified host.

        Args:
            host_id: int, host id.
            hostname: str, host name.
            networking_global_setting: dict, global network setting.
            roles: list of str, roles the host act as in the cluster.
            <security_name>_username: str, username of the <security_name>.
            <security_name>_password: str, password of the <security_name>.
            <interface_name>_interface: dict network interface configuration
                                        for <interface_name>.
            <partition_name>_partition_percentage: float, partition percentage
                                                   for <partition_name>.
            <partition_name>_partition_mbytes: int, partition mbytes for
                                               <partition_name>

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                    }
            error: status_code = 404 (ObjectDoesNotExist)
                                 400 (UserInvalidUsage,  InputMissingError)
                   resp_obj = {
                       'satus': '...',
                       'message': '...',
                   }
        '''
        data = {}
        if hostname:
            data['hostname'] = hostname

        if networking_global_setting:
            data.setdefault('networking', {})['global'] = (
                networking_global_setting)

        networking_interfaces = self.parse_networks(kwargs)
        if networking_interfaces:
            data.setdefault('networking', {})['interfaces'] = (
                networking_interfaces)

        security = self.parse_security(kwargs)
        if security:
            data['security'] = security

        partition = self.parse_partition(kwargs)
        if partition:
            data['partition'] = partition

        if roles:
            data['roles'] = roles

        return self.put('/api/clusterhosts/%s/config' % host_id, data)

    def delete_from_host_config(self, host_id, delete_key):
        '''
           Deletes one of editable attributes (as sub_key)
           in config for the specified host.

        Args:
            host_id: int, host id.
            delete_key: str, the key in config to delete.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                    }
            error: status_code = 404 (ObjectDoesNotExist)
                                 400 (UserInvalidUsage)
                   resp_obj = {
                       'satus': '...',
                       'message': '...',
                   }
        '''
        return self.delete('/api/clusterhosts/%s/config/%s' % (
            host_id, delete_key))

    def get_adapters(self, name=None):
        '''Lists details for the specified adapters by name.

        Args:
            name: string, adapter name.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'adapters': [{
                            'id': 1,
                            'name': 'CentOS_Openstack',
                            'os': 'CentOS',
                            'target_system': 'Openstack',
                        }]
                    }
        '''
        params = {}
        if name:
            params['name'] = name

        return self.get('/api/adapters', params=params)

    def get_adapter(self, adapter_id):
        '''Lists details for the specified adapter.

        Args:
            adapter_id: int, adapter id.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'adapter': {
                            'id': 1,
                            'name': 'CentOS_Openstack',
                            'os': 'CentOS',
                            'target_system': 'Openstack',
                        }
                    }
            error: status_code = 404 (ObjectDoesNotExist)
                   resp_obj = {
                       'status': '...',
                       'message': '...',
                   }
        '''
        return self.get('/api/adapters/%s' % adapter_id)

    def get_adapter_roles(self, adapter_id):
        '''Lists details of roles for the specified adapter

        Args:
            adapter_id: int, adapter id.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'roles': [{
                            'name': '...',
                            'description': '...',
                        }]
                    }
            error': status_code = 404 (ObjectDoesNotExist)
                    resp_obj = {
                        'status': '...',
                        'message': '...'
                    }
        '''
        return self.get('/api/adapters/%s/roles' % adapter_id)

    def get_host_installing_progress(self, host_id):
        '''Lists progress details for the specified host.

        Args:
            host_id: int, host id.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'progress': {
                            'id': 10,
                            'state': 'INSTALLING',
                            'percentage': 0.3,
                            'message': '...',
                            'severity': 'INFO',
                        }
                    }
            error: status_code = 404 (ObjectDoesNotExist)
                   resp_obj = {
                       'status': '...',
                       'message': '...',
                   }
        '''
        return self.get('/api/clusterhosts/%s/progress' % host_id)

    def get_cluster_installing_progress(self, cluster_id):
        '''Lists progress details for the specified cluster.

        Args:
            cluster_id: int, cluster id.

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'progress': {
                            'id': 10,
                            'state': 'INSTALLING',
                            'percentage': 0.3,
                            'messages': ['...'],
                            'severity': 'INFO',
                        }
                    }
            error: status_code = 404 (ObjectDoesNotExist)
                   resp_obj = {
                       'status': '...',
                       'message': '...',
                   }
        '''

        return self.get('/api/clusters/%s/progress' % cluster_id)

    def get_dashboard_links(self, cluster_id):
        '''
           Lists links for dashboards of the systems deployed
           on the specified cluster successfully

        Args:
            cluster_id: int, cluster id

        Returns:
            status_code as int, resp_obj as dict.
            normal: status_code = 200
                    resp_obj = {
                        'status': 'OK',
                        'dashboardlinks': {
                            '<role-name>': '<dashboard link>',
                        }
                    }
            error: status_code = 404 (ObjectDoesNotExist)
                   resp_obj = {
                       'status': '...',
                       'message': '...'
                   }
        '''
        params = {}
        params['cluser_id'] = cluster_id
        return self.get('/api/dashboardlinks', params)
