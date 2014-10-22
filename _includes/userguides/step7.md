<h2 id="step-seven">Step 7 - Networking</h2>

In this step, you can configure your cluster's network.

You can see in the page below, there are 4 interfaces listed for the host machine by default. You need to cross out "eth2" and "eth3" by clicking on the "x" on top of them. Then click on "Autofill" to automatically add subnets and fill in IP addresses. 

![Networking](/img/appliance/7_network-1.png)

You should be able to see configuration for two interfaces now. Please use "eth0" as Management interface by checking the box of "eth0" under "Is mgmt". Also please set "eth1" in "promiscuous mode". The promiscuous mode is for openstack-neutron service to assign floating IPs. So in this case, "eth1" will be your OpenStack external/public network.

![subnets](/img/appliance/7_subnet.png)

Now click on "Add subnet" to add a subnet for each interface. Please use the config shown below.

![add subnets](/img/appliance/7_addsubnet.png)

Click "OK" when you have finished. Now you will see that two subnets have already been created. Please make sure *"33.33.33.0/24"* is mapped to *"eth0"* and *"192.168.100.0/24"* is mapped to *"eth1"*. You can use the drop-down menu to change the mapping.

Now please fill in IP start values for two interfaces. Compass uses '33.33.33.10 and 33.33.33.20'. You may go with other IPs. Please refer to the image below for configuring IP addresses. The drop-down menu next to the IP start field is for IP address auto-fill rules. It provides incremental rules for IP addresses assignment if there are multiple servers. This setting won't affect our cluster as we only have one all-in-one server.

Also on the left, there is a drop-down menu for assigning hostnames with patterns. We currently provide two patterns.

![auto fill subnet](/img/appliance/7_autofill-subnet.png)

Click on "Fill Values". You will see the IPs and hostname have been assigned to the server.

![ip filled](/img/appliance/7_filled-ips.png)

Proceed with the "Next" button.

**OpenStack Networks: **As you may have noticed, besides "Global", there are four other tabs:

  * Management: The management network used by OpenStack for various management purposes, such as service endpoint authorization, component communication, etc;

  * Tenant: The OpenStack tenant network. This network enables OpenStack tenants(virtual machines) that are from different physical compute nodes to communicate with each other;

  * External: The external network is a network which OpenStack neutron routes tenant public traffic to. This requires the respective physical interface to be set as promiscuous mode. That is to say, this network needs to be mapped to a unique physical interface which is different from all other networks to avoid networking chaos. (please refer to the screenshot below)

  * Storage: Currently the storage network is not utilized by Compass. Theoretically the storage network will be used by tenants to access storage devices or services such as Swift/Cinder;

