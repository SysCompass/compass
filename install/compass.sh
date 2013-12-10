#!/bin/bash

source install.conf
SCRIPT_DIR=$(cd $(dirname "$0") && pwd)
cd $SCRIPT_DIR
# sudo \cp -rf ../../compass_flask/* $COMPASS_HOME


# download dependences
wget http://github.com/downloads/bitovi/javascriptmvc/$JS_MVC.zip
sudo yum install -y unzip
sudo unzip $JS_MVC
sudo \cp -rf $JS_MVC/. ../web/public/

# update squid conf
sudo rm /etc/squid/squid.conf 
# sudo ln -s $COMPASS_HOME/installers/os/config/squid.conf /etc/squid/squid.conf
sudo cp ../misc/squid/squid.conf /etc/squid/
sudo chmod 644 /etc/squid/squid.conf
sudo mkdir -p /var/squid/cache
sudo chown -R squid:squid /var/squid
sudo service squid restart

# Install net-snmp
# sudo yum install -y net-snmp-utils net-snmp
if [ ! -d "/usr/local/share/snmp/" ]; then
  sudo mkdir /usr/local/share/snmp/
fi
sudo cp -rf ../mibs /usr/local/share/snmp/
sudo cat >> /etc/snmp/snmp.conf <<EOF
mibdirs +/usr/local/share/snmp/mibs
EOF

# update cobbler config
sudo cp -r /var/lib/cobbler/snippets /root/backup/cobbler/
sudo cp -r /var/lib/cobbler/kickstarts/ /root/backup/cobbler/
sudo rm -rf /var/lib/cobbler/snippets/*
sudo cp -r ../misc/cobbler/snippets/* /var/lib/cobbler/snippets/
sudo chmod 777 /var/lib/cobbler/snippets
sudo chmod 666 /var/lib/cobbler/snippets/*
sudo rm /var/lib/cobbler/kickstarts/default.ks
sudo cp -r ../misc/cobbler/kickstarts/default.ks /var/lib/cobbler/kickstarts/
sudo chmod 666 /var/lib/cobbler/kickstarts/default.ks

# update chef config
sudo mkdir -p /var/chef/cookbooks/
sudo mkdir -p /var/chef/databags/
sudo mkdir -p /var/chef/roles/

sudo cp -r ../misc/chef/cookbooks/* /var/chef/cookbooks/
sudo cp -r ../misc/chef/databags/* /var/chef/databags/
sudo cp -r ../misc/chef/roles/* /var/chef/roles/


sudo knife cookbook upload --all --cookbook-path /var/chef/cookbooks/
sudo knife data bag create openstack
sudo knife data bag from file openstack /var/chef/databags/openstack/openstack.json

/opt/compsas/bin/addcookbooks.py
/opt/compass/bin/adddatabags.py
/opt/compass/bin/addroles.py

# Move files to their respective locations
mkdir -p /etc/compass
mkdir -p /opt/compass/bin
mkdir -p /var/www/compass_web
mkdir -p /var/log/compass
mkdir -p /opt/compass/db
mkdir -p /var/www/compass

sudo \cp -rf ../misc/apache/ods-server /etc/httpd/conf.d/ods-server.conf
sudo \cp -rf ../misc/apache/compass.wsgi /var/www/compass/compass.wsgi
sudo \cp -rf ../conf/celeryconfig /etc/compass/
sudo \cp -rf ../conf/global_config /etc/compass/
sudo \cp -rf ../conf/setting /etc/compass/
sudo \cp -rf ../conf/compassd /etc/init.d/
sudo \cp -rf ../bin/*.py /opt/compass/bin/
sudo \cp -rf ../bin/*.sh /opt/compass/bin/
sudo \cp -rf ../bin/chef/* /opt/compass/bin/
sudo \cp -rf ../bin/compassd /usr/bin/
sudo \cp -rf ../web/public/* /var/www/compass_web/
sudo chmod +x /etc/init.d/compassd
sudo chmod +x /usr/bin/compassd
 
# setup ods server
sudo yum -y install openssl
sudo yum -y install openssl098e
sudo cp -r /usr/lib64/libcrypto.so.6 /usr/lib64/libcrypto.so 
sudo chmod -R 777 /var/log/compass
sudo echo "export C_FORCE_ROOT=1" > /etc/profile.d/celery_env.sh
sudo chmod +x /etc/profile.d/celery_env.sh
sudo service httpd restart
cd ..
sudo python setup.py install
figlet -ctf slant Installation Complete!
