#!/bin/bash

source install.conf

sudo figlet Compass
sudo figlet Installer
WRITEDHCP()
{
    varname=${1,,}
    echo "Setting up $varname"
    eval var=\$$(echo $1)

    if [[ -z $var ]]; then
        echo "Setting up DHCP $varname"
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
echo $range
WRITEDHCP SUBNET $(ipcalc $(ip address| grep 'global eth0' |cut -f 6 -d ' ') -n|cut -f 2 -d '=')
WRITEDHCP OPTION_ROUTER $ipaddr
WRITEDHCP IP_RANGE "$range"
WRITEDHCP NEXTSERVER $ipaddr

echo "***************"
echo "subnet: $SUBNET"
echo "option_router: $OPTION_ROUTER"
echo "ip_range: $IP_RANGE"
echo "next_server: $NEXTSERVER"
