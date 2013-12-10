source install.conf
echo "Installing cobbler related packages"
sudo yum -y install cobbler cobbler-web createrepo mkisofs python-cheetah  python-simplejson python-urlgrabber PyYAML Django cman debmirror pykickstart -y

sudo chkconfig cobblerd on

# create backup dir
sudo mkdir /root/backup # create backup folder

# configure ntp
sudo cp /etc/ntp.conf /root/backup/
# update ntp.conf
sudo sed -i 's/^#server[ \t]\+127.127.1.0/server 127.127.1.0/g' /etc/ntp.conf
sudo sed -i 's/^#fudge[ \t]\+127.127.1.0/fudge 127.127.1.0/g' /etc/ntp.conf
sudo service ntpd restart

# configure xinetd
sudo cp /etc/xinetd.d/tftp /root/backup/
sudo sed -i 's/disable\([ \t]\+\)=\([ \t]\+\)yes/disable\1=\2no/g' /etc/xinetd.d/tftp
sudo service xinetd restart

export ipaddr=$(ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
export cobbler_passwd=$(openssl passwd -1 -salt 'huawei' '123456')

# configure dhcpd
SUBNET=${SUBNET:-$(ipcalc $(ip address| grep 'global eth0' |cut -f 6 -d ' ') -n|cut -f 2 -d '=')}

OPTION_ROUTER=${OPTION_ROUTER:-$(ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')}

IPRANGE=${IPRANGE:-$(echo "$(echo "$ipaddr"|cut -f 1 -d '.').$(echo "$ipaddr"|cut -f 2 -d '.').$(echo "$ipaddr"|cut -f 3 -d '.').100 $(echo "$ipaddr"|cut -f 1 -d '.').$(echo "$ipaddr"|cut -f 2 -d '.').$(echo "$ipaddr"|cut -f 3 -d '.').254")}

NEXTSERVER=${NEXTSERVER:-$ipaddr}

sudo mkdir /root/backup/cobbler
sudo cp /etc/cobbler/settings /root/backup/cobbler/
sudo cp /etc/cobbler/dhcp.template /root/backup/cobbler/

# Dumps the variables to dhcp template
sudo sed -i "s/subnet 192.168.1.0 netmask 255.255.255.0/subnet $SUBNET netmask 255.255.255.0/g" /etc/cobbler/dhcp.template
sudo sed -i "/option routers/c\     option routers             $OPTION_ROUTER;" /etc/cobbler/dhcp.template
sudo sed -i "/range dynamic-bootp/c\     range dynamic-bootp        $IPRANGE;" /etc/cobbler/dhcp.template
sudo sed -i "/next-server/c\     next-server                $NEXTSERVER;" /etc/cobbler/dhcp.template

# Set up other setting options in cobbler/settings
sudo sed -i "/next_server/c\next_server: $ipaddr" /etc/cobbler/settings
sudo sed -i "s/server:[ \t]\+127.0.0.1/server: $ipaddr/g" /etc/cobbler/settings
sudo sed -i 's/manage_dhcp:[ \t]\+0/manage_dhcp: 1/g' /etc/cobbler/settings
sudo sed -i 's/manage_dns:[ \t]\+0/manage_dns: 1/g' /etc/cobbler/settings
sudo sed -i 's/manage_tftpd:[ \t]\+0/manage_tftpd: 1/g' /etc/cobbler/settings
sudo sed -i 's/anamon_enabled:[ \t]\+0/anamon_enabled: 1/g' /etc/cobbler/settings
sudo sed -i "s/default_name_servers:.*/default_name_servers: \['$ipaddr'\]/g" /etc/cobbler/settings
sudo sed -i 's/enable_menu:[ \t]\+1/enable_menu: 0/g' /etc/cobbler/settings
sudo sed -i "s/manage_forward_zones:.*/manage_forward_zones: \['ods.com'\]/g" /etc/cobbler/settings
sudo sed -i 's/pxe_just_once:[ \t]\+0/pxe_just_once: 1/g' /etc/cobbler/settings
sudo sed -i "s,^default_password_crypted:[ \t]\+\"\(.*\)\",default_password_crypted: \"$cobbler_passwd\",g" /etc/cobbler/settings
sudo sed -i 's/^RewriteRule/# RewriteRule/g' /etc/httpd/conf.d/cobbler_web.conf
sudo sed -i 's/^Listen\([ \t]\+\)443/Listen\1445/g' /etc/httpd/conf.d/ssl.conf
sudo sed -i 's/^<VirtualHost\(.*\):443>/<VirtualHost\1:445>/g' /etc/httpd/conf.d/ssl.conf


sudo mkdir /root/backup/selinux
sudo cp /etc/selinux/config /root/backup/selinux/
sudo sed -i '/SELINUX/s/enforcing/disabled/' /etc/selinux/config

sudo cp /etc/cobbler/modules.conf /root/backup/cobbler/
sudo sed -i 's/module\([ \t]\+\)=\([ \t]\+\)authn_denyall/module\1=\2authn_configfile/g' /etc/cobbler/modules.conf

echo "setting up cobbler web password: default user is cobbler"

CBLR_USER=${CBLR_USER:-"cobbler"}
CBLR_PASSWD=${CBLR_PASSWD:-"cobbler"}
(echo -n "$CBLR_USER:Cobbler:" && echo -n "$CBLR_USER:Cobbler:$CBLR_PASSWD" | md5sum - | cut -d' ' -f1) >> /etc/cobbler/users.digest

sudo sed -i "s/listen-on[ \t]\+.*;/listen-on port 53 \{ $ipaddr; \};/g" /etc/cobbler/named.template
sudo sed -i 's/allow-query[ \t]\+.*/allow-query\t{ 127.0.0.0\/8; 10.0.0.0\/8; 192.168.0.0\/16; 172.16.0.0\/12; };/g' /etc/cobbler/named.template

echo "$HOSTNAME A $ipaddr" >> zone.template

sudo cp /etc/xinetd.d/rsync /root/backup/
sudo sed -i 's/disable\([ \t]\+\)=\([ \t]\+\)yes/disable\1=\2no/g' /etc/xinetd.d/rsync
sudo sed -i 's/^@dists=/# @dists=/g' /etc/debmirror.conf
sudo sed -i 's/^@arches=/# @arches=/g' /etc/debmirror.conf

echo "Checking if httpd is running"
sudo ps cax | grep httpd > /dev/null
if [ $? -eq 0 ]; then
  echo "httpd is running."
else
  echo "httpd is not running. Starting httpd"
  sudo service httpd start
fi

sudo service cobblerd restart
sudo cobbler get-loaders
sudo cobbler check
sudo cobbler sync

echo "Checking if dhcpd is running"
sudo ps cax | grep dhcpd > /dev/null
if [ $? -eq 0 ]; then
  echo "dhcpd is running."
else
  echo "dhcpd is not running. Starting httpd"
  sudo service dhcpd start
fi

echo "Checking if named is running"
ps cax | grep named > /dev/null
if [ $? -eq 0 ]; then
  echo "named is running."
else
  echo "named is not running. Starting httpd"
  sudo service named start
fi

# import cobbler distro
export ipaddr=$(ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
sudo mkdir /var/lib/cobbler/iso
sudo curl "$IMAGE_SOURCE" > /var/lib/cobbler/iso/CentOS6.4-minimal.iso
sudo mkdir -p /mnt/CentOS6.4-minimal
sudo mount -t auto -o loop /var/lib/cobbler/iso/CentOS6.4-minimal.iso /mnt/CentOS6.4-minimal
sudo cobbler import --path=/mnt/CentOS6.4-minimal --name=CentOS6.4-minimal --arch=x86_64
# manually run distro add and profile add if cobbler import fails
sudo cobbler distro add --name=CentOS6.4-minimal --kernel=/var/www/cobbler/ks_mirror/CentOS6.4-minimal-x86_64/isolinux/vmlinuz --initrd=/var/www/cobbler/ks_mirror/CentOS6.4-minimal-x86_64/isolinux/initrd.img --arch=x86_64 --breed=redhat
sudo cobbler profile add --name=CentOS6.4-minimal --repo=ppa_repo --distro=CentOS6.4-minimal --ksmeta= "tree=http://$ipaddr/cobbler/ks_mirror/CentOS6.4-minimal" --kickstart=/var/lib/cobbler/kickstarts/default.ks

# create repo
sudo mkdir -p /var/lib/cobbler/repo_mirror/ppa_repo
sudo cobbler repo add --mirror=/var/lib/cobbler/repo_mirror/ppa_repo --name=ppa_repo --mirror-locally=Y
# download packages
cd /var/lib/cobbler/repo_mirror/ppa_repo/
sudo curl http://opscode-omnibus-packages.s3.amazonaws.com/el/6/x86_64/chef-11.8.0-1.el6.x86_64.rpm > chef-11.8.0-1.el6.x86_64.rpm

sudo curl ftp://rpmfind.net/linux/centos/6.4/os/x86_64/Packages/ntp-4.2.4p8-3.el6.centos.x86_64.rpm > ntp-4.2.4p8-3.el6.centos.x86_64.rpm

sudo curl ftp://rpmfind.net/linux/centos/6.4/os/x86_64/Packages/openssh-clients-5.3p1-84.1.el6.x86_64.rpm > openssh-clients-5.3p1-84.1.el6.x86_64.rpm

sudo curl ftp://rpmfind.net/linux/centos/6.4/os/x86_64/Packages/iproute-2.6.32-23.el6.x86_64.rpm > iproute-2.6.32-23.el6.x86_64.rpm

sudo curl ftp://rpmfind.net/linux/centos/6.4/os/x86_64/Packages/wget-1.12-1.8.el6.x86_64.rpm > wget-1.12-1.8.el6.x86_64.rpm
cd ..
sudo createrepo ppa_repo
sudo cobbler reposync

echo "Cobbler configuration complete!"
