#!/bin/bash
/opt/compass/bin/clean_clusters.py
/opt/compass/bin/manage_db.py createdb
/opt/compass/bin/manage_db.py sync_from_installers
/opt/compass/bin/manage_db.py set_fake_switch_machine
service compassd restart
service httpd restart
service rsyslog restart
