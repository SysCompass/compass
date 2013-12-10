#!/bin/bash
sudo rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm > /dev/null
sed -i 's/^mirrorlist=https/mirrorlist=http/g' /etc/yum.repos.d/epel.repo
sudo yum -y install figlet > /dev/null
figlet -ctf slant Compass Installer

source install.conf

errtrap()
{
    echo "[FILE: "${BASH_SOURCE[0]}", LINE: $1] Error: Command or function exited with status $?"
}

trap 'errtrap $LINENO' ERR

loadvars()
{
    varname=${1,,}
    eval var=\$$(echo $1)

    if [[ -z $var ]]; then
        echo "Please enter the DHCP $varname (Example: $2) "
        while read input
        do
            if [ "$input" == "" ]; then
                echo "Default $varname chosen"
                export $(echo $1)="$2"
                break
            elif [[ "$input" != *.* ]]; then
                echo "I really expect IP addresses"
            else
                echo "You have entered $input"
                export $(echo $1)=$input
                break
            fi
        done
    fi
}

export ipaddr=$(ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
range=$(echo "$(echo "$ipaddr"|cut -f 1 -d '.').$(echo "$ipaddr"|cut -f 2 -d '.').$(echo "$ipaddr"|cut -f 3 -d '.').100 $(echo "$ipaddr"|cut -f 1 -d '.').$(echo "$ipaddr"|cut -f 2 -d '.').$(echo "$ipaddr"|cut -f 3 -d '.').254")
loadvars SUBNET $(ipcalc $(ip address| grep 'global eth0' |cut -f 6 -d ' ') -n|cut -f 2 -d '=')
loadvars OPTION_ROUTER $ipaddr
loadvars IP_RANGE "$range"
loadvars NEXTSERVER $ipaddr



echo "Install the Dependencies"
sudo bash dependency.sh

echo "Install the OS Installer Tool"
sudo bash $OS_INSTALLER.sh

echo "Install the Package Installer Tool"
sudo bash $PACKAGE_INSTALLER.sh

echo "Download and Setup Compass and related services"
sudo bash compass.sh
