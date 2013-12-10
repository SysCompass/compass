'''database model.'''
from datetime import datetime
import simplejson as json
import logging
import uuid
from sqlalchemy import Column, ColumnDefault, Integer, String
from sqlalchemy import Float, Enum, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from compass.utils import util


BASE = declarative_base()


class Switch(BASE):
    '''Switch table.
    
    id: identity: int as primary key.
    ip: string as xxx.xxx.xxx.xxx format. unique.
    vendor_info: string. vendor information.
                 It should not be used directly.
    credential_data: string. stores the credential data in json format.
                     It should not be used directly.
    state: Enum. 'not_reached': snmp fails to get switch info.,
           'under_monitoring': the switch info is already got.
    machines: refer to list of Machine connected to the switch.
    '''
    __tablename__ = 'switch'

    id = Column(Integer, primary_key=True)
    ip = Column(String(80), unique=True)
    credential_data = Column(Text)
    vendor_info = Column(String(256), nullable=True)
    state = Column(Enum('not_reached', 'under_monitoring',
                        name='switch_state'))

    def __init__(self, **kwargs):
        self.state = 'not_reached'
        super(Switch, self).__init__(**kwargs)

    def __repr__(self):
        return '<Switch ip: %r, credential: %r, vendor: %r, state: %s>'\
            % (self.ip, self.credential, self.vendor, self.state)

    @property
    def vendor(self):
        '''vendor property getter'''
        return self.vendor_info

    @vendor.setter
    def vendor(self, value):
        '''vendor property setter'''
        self.vendor_info = value

    @property
    def credential(self):
        '''credential data getter.

        Returns:
            python primitive object.
        '''
        if self.credential_data:
            try:
                credential = json.loads(self.credential_data)
                credential = dict(
                    [(str(k).title(), str(v)) for k, v in credential.items()])
                return credential
            except Exception as error:
                logging.error('failed to load credential data %s: %s',
                              self.id, self.credential_data)
                logging.exception(error)
                return {}
        else:
            return {}

    @credential.setter
    def credential(self, value):
        '''credential property setter
        
        Args:
            python primitive object.
    
        Returns:
            None
        '''
        if value:
            try:
                credential = {}
                if self.credential_data:
                    credential = json.loads(self.credential_data)

                credential.update(value)
                self.credential_data = json.dumps(credential)

            except Exception as error:
                logging.error('failed to dump credential data %s: %s',
                              self.id, value)
                logging.exception(error)
        else:
            self.credential_data = json.dumps({})
        logging.debug('switch now is %s', self)


class Machine(BASE):
    """
      Note: currently, we are taking care of management plane.
            Therefore, we assume one machine is connected to one switch.
      id: int, identity as primary key
      mac: string, mac address of this machine in xx:xx:xx:xx:xx:xx format,
           unique.
      switch_id: switch id that this machine connected on to.
      port: nth port of the switch that this machine connected.
      vlan: vlan id that this machine connected on to.
      update_timestamp: last time this entry got updated.
      switch: refer to the Switch the machine connects to.
    """
    __tablename__ = 'machine'

    id = Column(Integer, primary_key=True)
    mac = Column(String(24), unique=True)
    port = Column(Integer)
    vlan = Column(Integer)
    update_timestamp = Column(DateTime, default=datetime.now,
                              onupdate=datetime.now)
    switch_id = Column(Integer, ForeignKey('switch.id',
                                           onupdate='CASCADE',
                                           ondelete='SET NULL'))
    switch = relationship('Switch', backref=backref('machines',
                                                    lazy='dynamic'))

    def __init__(self, **kwargs):
        super(Machine, self).__init__(**kwargs)

    def __repr__(self):
        return '<Machine %r: port=%r vlan=%r switch=%r>'\
            % (self.mac, self.port, self.vlan, self.switch)


class HostState(BASE):
    '''the state of the ClusterHost.
 
    id: int, identity as primary key.
    state: Enum. 'UNINITIALIZED': the host is ready to setup.
                 'INSTALLING': the host is not installing.
                 'READY': the host is setup.
                 'ERROR': the host has error.
    progress: float, the installing progress from 0 to 1.
    message: the latest installing message.
    severity: Enum, the installing message severity.
              Should be in one of ['INFO', 'WARNING', 'ERROR'].
    update_timestamp: the lastest timestamp the entry got updated.
    host: refer to ClusterHost.
    '''
    __tablename__ = "host_state"

    id = Column(Integer, ForeignKey('cluster_host.id',
                                    onupdate='CASCADE',
                                    ondelete='CASCADE'),
                primary_key=True)
    state = Column(Enum('UNINITIALIZED', 'INSTALLING', 'READY', 'ERROR'),
                   ColumnDefault('UNINITIALIZED'))
    progress = Column(Float, ColumnDefault(0.0))
    message = Column(String)
    severity = Column(Enum('INFO', 'WARNING', 'ERROR'), ColumnDefault('INFO'))
    update_timestamp = Column(DateTime, default=datetime.now,
                              onupdate=datetime.now)
    host = relationship('ClusterHost', backref=backref('state',
                                                       uselist=False))

    def __init__(self, **kwargs):
        super(HostState, self).__init__(**kwargs)

    @property
    def hostname(self):
        '''hostname getter'''
        return self.host.hostname

    def __repr__(self):
        return ('<HostState %r: state=%r, progress=%s, '
                   'message=%s, severity=%s>') % (
            self.hostname, self.state, self.progress,
            self.message, self.severity)


class ClusterState(BASE):
    '''The state of the Cluster.

    id: int, identity as primary key.
    state: Enum, 'UNINITIALIZED': the cluster is ready to setup.
                 'INSTALLING': the cluster is not installing.
                 'READY': the cluster is setup.
                 'ERROR': the cluster has error.
    progress: float, the installing progress from 0 to 1.
    message: the latest installing message.
    severity: Enum, the installing message severity.
              Should be in one of ['INFO', 'WARNING', 'ERROR'].
    update_timestamp: the lastest timestamp the entry got updated.
    cluster: refer to Cluster.
    '''
    __tablename__ = 'cluster_state'
    id = Column(Integer, ForeignKey('cluster.id',
                                    onupdate='CASCADE',
                                    ondelete='CASCADE'),
                primary_key=True)
    state = Column(Enum('UNINITIALIZED', 'INSTALLING', 'READY', 'ERROR'),
                   ColumnDefault('UNINITIALIZED'))
    progress = Column(Float, ColumnDefault(0.0))
    message = Column(String)
    severity = Column(Enum('INFO', 'WARNING', 'ERROR'), ColumnDefault('INFO'))
    update_timestamp = Column(DateTime, default=datetime.now,
                              onupdate=datetime.now)
    cluster = relationship('Cluster', backref=backref('state',
                                                      uselist=False))

    def __init__(self, **kwargs):
        super(ClusterState, self).__init__(**kwargs)

    @property
    def clustername(self):
        'clustername getter'
        return self.cluster.name

    def __repr__(self):
        return ('<ClusterState %r: state=%r, progress=%s, '
                   'message=%s, severity=%s>') % (
            self.clustername, self.state, self.progress,
            self.message, self.severity)


class Cluster(BASE):
    '''Cluster configuration information.
    
    id: int, identity as primary key.
    name: string, cluster name.
    mutable: bool, if the Cluster is mutable.
    security_config: string stores json formatted security information.
    networking_config: string stores json formatted networking information.
    partition_config: string stores json formatted parition information.
    adapter_id: the refer id in the Adapter table.
    raw_config: string stores json formatted other cluster information.
    adapter: refer to the Adapter.
    state: refer to the ClusterState.
    '''
    __tablename__ = 'cluster'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    mutable = Column(Boolean, default=True)
    security_config = Column(Text)
    networking_config = Column(Text)
    partition_config = Column(Text)
    adapter_id = Column(Integer, ForeignKey('adapter.id'))
    raw_config = Column(Text)
    adapter = relationship("Adapter", backref=backref('clusters',
                                                      lazy='dynamic'))

    def __init__(self, **kwargs):
        if 'name' not in kwargs or not kwargs['name']:
            self.name = str(uuid.uuid4())
            if 'name' in kwargs:
                del kwargs['name']
        super(Cluster, self).__init__(**kwargs)

    def __repr__(self):
        return '<Cluster %r: config=%r>' % (self.name, self.config)

    @property
    def partition(self):
        '''partition getter'''
        if self.partition_config:
            try:
                return json.loads(self.partition_config)
            except Exception as error:
                logging.error('failed to load security config %s: %s',
                              self.id, self.partition_config)
                logging.exception(error)
                return {}
        else:
            return {}

    @partition.setter
    def partition(self, value):
        '''partition setter'''
        logging.debug('cluster %s set partition %s', self.id, value)
        if value:
            try:
                self.partition_config = json.dumps(value)
            except Exception as error:
                logging.error('failed to dump partition config %s: %s',
                              self.id, value)
                logging.exception(error)
        else:
            self.partition_config = None

    @property
    def security(self):
        '''security getter'''
        if self.security_config:
            try:
                return json.loads(self.security_config)
            except Exception as error:
                logging.error('failed to load security config %s: %s',
                              self.id, self.security_config)
                logging.exception(error)
                return {}
        else:
            return {}

    @security.setter
    def security(self, value):
        '''security setter'''
        logging.debug('cluster %s set security %s', self.id, value)
        if value:
            try:
                self.security_config = json.dumps(value)
            except Exception as error:
                logging.error('failed to dump security config %s: %s',
                              self.id, value)
                logging.exception(error)
        else:
            self.security_config = None

    @property
    def networking(self):
        'networking getter'''
        if self.networking_config:
            try:
                return json.loads(self.networking_config)
            except Exception as error:
                logging.error('failed to load networking config %s: %s',
                              self.id, self.networking_config)
                logging.exception(error)
                return {}
        else:
            return {}

    @networking.setter
    def networking(self, value):
        '''networking setter'''
        logging.debug('cluster %s set networking %s', self.id, value)
        if value:
            try:
                self.networking_config = json.dumps(value)
            except Exception as error:
                logging.error('failed to dump networking config %s: %s',
                              self.id, value)
                logging.exception(error)
        else:
            self.networking_config = None

    @property
    def config(self):
        '''get config from security, networking, partition'''
        config = {}
        if self.raw_config:
            try:
                config = json.loads(self.raw_config)
            except Exception as error:
                logging.error('failed to load raw config %s: %s',
                              self.id, self.raw_config)
                logging.exception(error)
        util.mergeDict(config, {'security': self.security})
        util.mergeDict(config, {'networking': self.networking})
        util.mergeDict(config, {'partition': self.partition})
        util.mergeDict(config, {'clusterid': self.id,
                                'clustername': self.name})
        return config

    @config.setter
    def config(self, value):
        '''set config to security, networking, partition.'''
        logging.debug('cluster %s set config %s', self.id, value)
        if not value:
            self.security = None
            self.networking = None
            self.partition = None
            self.raw_config = None
            return
        self.security = value.get('security')
        self.networking = value.get('networking')
        self.partition = value.get('partition')
        try:
            self.raw_config = json.dumps(value)
        except Exception as error:
            logging.error('failed to dump raw config %s: %s',
                          self.id, value)
            logging.exception(error)


class ClusterHost(BASE):
    '''ClusterHost information.

    id: int, identity as primary key.
    machine_id: int, the id of the Machine.
    cluster_id: int, the id of the Cluster.
    mutable: if the ClusterHost information is mutable.
    hostname: str, host name.
    config_data: string, json formatted config data.
    cluster: refer to Cluster the host in.
    machine: refer to the Machine the host on.
    state: refer to HostState indicates the host state.
    '''
    __tablename__ = 'cluster_host'

    id = Column(Integer, primary_key=True)

    machine_id = Column(Integer, ForeignKey('machine.id',
                                            onupdate='CASCADE',
                                            ondelete='CASCADE'),
                        nullable=True)

    cluster_id = Column(Integer, ForeignKey('cluster.id',
                                            onupdate='CASCADE',
                                            ondelete='SET NULL'),
                        nullable=True)

    hostname = Column(String, unique=True)
    config_data = Column(Text)
    mutable = Column(Boolean, default=True)

    cluster = relationship("Cluster", backref=backref('hosts', lazy='dynamic'))
    machine = relationship("Machine", backref=backref('host', uselist=False))

    def __init__(self, **kwargs):
        if 'hostname' not in kwargs or not kwargs['hostname']:
            self.hostname = str(uuid.uuid4())
            if 'hostname' in kwargs:
                del kwargs['hostname']
        super(ClusterHost, self).__init__(**kwargs)

    def __repr__(self):
        return '<ClusterHost %r: cluster=%r machine=%r>'\
            % (self.hostname, self.cluster, self.machine)

    @property
    def config(self):
        '''config getter.'''
        config = {}
        if self.config_data:
            try:
                config.update(json.loads(self.config_data))
                config.update({'hostid': self.id, 'hostname': self.hostname})
                if self.cluster:
                    config.update({'clusterid': self.cluster.id,
                                   'clustername': self.cluster.name})
                if self.machine:
                    util.mergeDict(
                        config, {
                            'networking': {
                                'interfaces': {
                                    'management': {
                                        'mac': self.machine.mac
                                    }
                                }
                            }
                        })
            except Exception as error:
                logging.error('failed to load config %s: %s',
                              self.hostname, self.config_data)
                logging.exception(error)
        return config

    @config.setter
    def config(self, value):
        'config setter'''
        if not self.config_data:
            config = {
            }
            self.config_data = json.dumps(config)

        if value:
            try:
                config = json.loads(self.config_data)
                util.mergeDict(config, value)

                self.config_data = json.dumps(config)
            except Exception as error:
                logging.error('failed to dump config %s: %s',
                              self.hostname, value)
                logging.exception(error)


class LogProgressingHistory(BASE):
    '''host installing log history for each file.
   
    id: int, identity as primary key.
    pathname: str, the full path of the installing log file. unique.
    position: int, the position of the log file it has processed.
    partial_line: str, partial line of the log.
    progressing: float, indicate the installing progress between 0 to 1.
    message: string, str, the installing message.
    severity: Enum, the installing message severity.
              Should be in ['ERROR', 'WARNING', 'INFO']
    line_matcher_name: string, the line matcher name of the log processor.
    update_timestamp: datetime, the latest timestamp the entry got updated.
    '''
    __tablename__ = 'log_progressing_history'
    id = Column(Integer, primary_key=True)
    pathname = Column(String, unique=True)
    position = Column(Integer, ColumnDefault(0))
    partial_line = Column(Text)
    progress = Column(Float, ColumnDefault(0.0))
    message = Column(Text)
    severity = Column(Enum('ERROR', 'WARNING', 'INFO'), ColumnDefault('INFO'))
    line_matcher_name = Column(String, ColumnDefault('start'))
    update_timestamp = Column(DateTime, default=datetime.now,
                              onupdate=datetime.now)

    def __init__(self, **kwargs):
        super(LogProgressingHistory, self).__init__(**kwargs)

    def __repr__(self):
        return ('LogProgressingHistory[%r: position %r,'
                'partial_line %r,progress %r,message %r,'
                'severity %r]') % (
            self.pathname, self.position,
            self.partial_line,
            self.progress,
            self.message,
            self.severity)


class Adapter(BASE):
    '''Table stores ClusterHost installing Adapter information.

    id: int, identity as primary key.
    name: string, adapter name, unique.
    os: string, os name for installing the host.
    target_system: string, target system to be installed on the host.
                   Such as openstack.
    clusters: refer to the list of Cluster.
    '''
    __tablename__ = 'adapter'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    os = Column(String)
    target_system = Column(String)

    def __init__(self, **kwargs):
        super(Adapter, self).__init__(**kwargs)

    def __repr__(self):
        return '<Adapter %r: os %r, target_system %r>' % (
            self.name, self.os, self.target_system)


class Role(BASE):
    '''
    The Role table stores avaiable roles of one target system
    where the host can be deployed to one or several roles in the cluster.

    id: int, identity as primary key.
    name: role name.
    target_system: str, the target_system.
    description: str, the description of the role.
    '''
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    target_system = Column(String)
    description = Column(Text)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)

    def __repr__(self):
        return '<Role %r : target_system %r, description:%r>' % (
            self.name, self.target_system, self.description)
