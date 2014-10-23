<h2 id="step-eleven">Step 11 - Network Mapping</h2>

You have already configured physical networks in previous steps, now it's time to map the OpenStack logical networks to them. 

Compass provides four OpenStack networks:

  * Management: The management network used by OpenStack for various management purposes, such as service endpoint authorization, component communication, etc;

  * Tenant: The OpenStack tenant network. This network enables OpenStack tenants(virtual machines) that are from different physical compute nodes to communicate with each other;

  * External: The external network is a network which OpenStack neutron routes tenant public traffic to. This requires the respective physical interface to be set as promiscuous mode. That is to say, this network needs to be mapped to a unique physical interface which is different from all other networks to avoid networking chaos. (please refer to the screenshot below)

  * Storage: The storage network will be used by tenants to access storage devices or services. Also Storage services are using storage network to communicate.

![networks](/img/appliance/11_net-mapping.png)

We have already assigned Management network to eth0 and External network to eth1. Note that in this case there are only two network interfaces. Thus Storage and Tenant networks have to be assigned to eth0. As you can see from the image above, eth1 is set as promiscuous mode, so no network other than External network can be assigned to it.

![assigned_net](/img/appliance/11_network-final.png) 
