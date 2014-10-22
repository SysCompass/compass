<h2 id="step-ten">Step 10 - Network Mapping</h2>


We are now mapping the networks to interfaces we created in "Networking" step.
Different target systems have their specific networks. In this instruction, we are showing how to assign OpenStack networks to interfaces. There are four types of OpenStack networks:


+ Management network: this is self-explanatory. All "control plane" traffic goes through this network. For example, authentication, nova api request, database request and queue messaging, etc. Management network doesn not require a very large bandwidth.

+ Tenant network: Virtual machines created by OpenStack use this network to communicate with each other.

+ Storage network: This network is used for storage devices/components to communicate, such as failover, mirroring and load balancing. Typically storage network uses a relatively large bandwidth. So a 10g network interface is preferred if possible.

+ Public network. This network is only required to be assigned on the network node. Neutron uses the public network as the network for assigning floating IPs. We should map public network onto the promiscuous mode interface we created in "Network" step and isolate this network. 
So it is important that we DO NOT overlap any other networks with this network. The public network has to be absolutely isolated. Although only the network node needs to have a interface setup in promisc mode specifically for public network, we make this setting as a global config to avoid ambiguity.


Similar to role assignment, drag networks and drop them at interfaces.

![network](/img/install/10_network_mapping.png)

Click "Next" once you have made sure all networks are properly assigned and no network overlaps with the public network.
