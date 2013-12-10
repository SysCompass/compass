#!/usr/bin/python
import logging
import os
import os.path
import sys

from flask.ext.script import Manager

from compass.api import app
from compass.config_management.utils import config_manager
from compass.db import database
from compass.db.model import Adapter, Role, Switch, Machine, HostState, ClusterState, Cluster, ClusterHost, LogProgressingHistory    
from compass.utils import flags
from compass.utils import logsetting
from compass.utils import setting_wrapper as setting


flags.add('table_name',
          help='table name',
          default='')


manager = Manager(app, usage="Perform database operations")


TABLE_MAPPING = {
    'role': Role,
    'adapter': Adapter,
    'switch': Switch,
    'machine': Machine,
    'hoststate': HostState,
    'clusterstate': ClusterState,
    'cluster': Cluster,
    'clusterhost': ClusterHost,
    'logprogressinghistory': LogProgressingHistory,
}


@manager.command
def list_config():
    "List the configuration"
    for key, value in app.config.items():
        print key, value


@manager.command
def createdb():
    "Creates database tables from sqlalchemy models"
    if setting.DATABASE_TYPE == 'sqlite':
        if os.path.exists(setting.DATABASE_FILE):
            os.remove(setting.DATABASE_FILE)
    database.create_db()
    if setting.DATABASE_TYPE == 'sqlite':
        os.chmod(setting.DATABASE_FILE, 0777)

@manager.command
def dropdb():
    "Creates database tables from sqlalchemy models"
    database.drop_db()


@manager.command
def createtable():
    table_name = flags.OPTIONS.table_name
    if table_name and table_name in TABLE_MAPPING:
        database.create_table(TABLE_MAPPING[table_name])
    else:
        print '--table_name should be in %s' % TABLE_MAPPING.keys()



              
@manager.command
def droptable():
    table_name = flags.OPTIONS.table_name
    if table_name and table_name in TABLE_MAPPING:
        database.drop_table(TABLE_MAPPING[table_name])
    else:
        print '--table_name should be in %s' % TABLE_MAPPING.keys()


@manager.command
def sync_from_installers():
    manager = config_manager.ConfigManager()
    adapters = manager.getAdapters()
    target_systems = set()
    roles_per_target_system = {}
    for adapter in adapters:
        target_systems.add(adapter['target_system'])
    for target_system in target_systems:
        roles_per_target_system[target_system] = manager.getRoles(target_system)
    with database.session() as session:
        session.query(Adapter).delete()
        session.query(Role).delete()
        for adapter in adapters:
            session.add(Adapter(**adapter))
        for target_system, roles in roles_per_target_system.items():
            for role in roles:
                session.add(Role(**role))
 

@manager.command
def set_fake_switch_machine():
    with database.session() as session:
        credential = { 'version'    :  'v2c',
                       'community'  :  'public',
                     }
        switches = [ {'ip': '192.168.100.250'},
                     {'ip': '192.168.100.251'},
                     {'ip': '192.168.100.252'},
        ]
        session.query(Switch).delete()
        session.query(Machine).delete()
        ip_switch ={}
        for item in switches:
            logging.info('add switch %s', item)     
            switch = Switch(ip=item['ip'], vendor_info='huawei',
                            state='under_monitoring')
            switch.credential = credential
            session.add(switch)
            ip_switch[item['ip']] = switch
        session.flush()

        machines = [
            {'mac': '00:0c:29:32:76:85', 'port':50, 'vlan':1, 'switch_ip':'192.168.100.250'},
            {'mac': '00:0c:29:fa:cb:72', 'port':51, 'vlan':1, 'switch_ip':'192.168.100.250'},
            {'mac': '28:6e:d4:64:c7:4a', 'port':1, 'vlan':1, 'switch_ip':'192.168.100.251'},
            {'mac': '28:6e:d4:64:c7:4c', 'port':2, 'vlan':1, 'switch_ip':'192.168.100.251'},
            {'mac': '28:6e:d4:46:c4:25', 'port': 40, 'vlan': 1, 'switch_ip': '192.168.100.252'},
            {'mac': '26:6e:d4:4d:c6:be', 'port': 41, 'vlan': 1, 'switch_ip': '192.168.100.252'},
            {'mac': '28:6e:d4:62:da:38', 'port': 42, 'vlan': 1, 'switch_ip': '192.168.100.252'},
            {'mac': '28:6e:d4:62:db:76', 'port': 43, 'vlan': 1, 'switch_ip': '192.168.100.252'},
        ]
       
        for item in machines:
            logging.info('add machine %s', item)
            machine = Machine(mac=item['mac'], port=item['port'],
                              vlan=item['vlan'],
                              switch_id=ip_switch[item['switch_ip']].id)
            session.add(machine)

 
if __name__ == "__main__":
    flags.init()
    logsetting.init()
    manager.run()
