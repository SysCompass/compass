<h2 id="step-seven">Step 7 - Networking</h2>

Networking enables OpenStack networking configuration. In this page, you may configure your OpenStack cluster's network by specifying global network configuration and per-interface network configuration.

![Networking](/img/7_networking.png)

**Global: **In the Global tab of Networking page, you will need to fill in these values:

  * DNS: The Domain-name server IP.
  * Search-path: A list of domains to specify for programs to translate a domain name into an IP address
  * Gateway: The global gateway to route host traffic to the outside network. 
  * HTTP proxy server: an HTTP proxy server for all HTTP traffic. This is very import as Compass uses HTTP proxy server to cache packages during host installation.


**Per-Interface Network: **There are four network types: Management, Tenant, Public and Storage. Each network interface type has a tab on the Networking page. These tabs have identical fields for you to fill in, which are:

  * IP-start: Compass Web UI intelligently assigns IP addresses. With given IP-start and IP-end values, every server selected in Servers page will be assigned with a unique IP address. So you will need to fill in a starting IP address here;
  * IP-end: As stated above, this field should be filled in with an ending IP address;
  * Netmask: The subnetmask for each network, default is 255.255.255.0 unless otherwise indicated; 
  * NIC: The physical interface number on each server for OpenStack to map its networks to.


**OpenStack Networks: **As you may have noticed, besides "Global", there are four other tabs:

  * Management: The management network used by OpenStack for various management purposes, such as service endpoint authorization, component communication, etc;
  * Tenant: The OpenStack tenant network. This network enables OpenStack tenants(virtual machines) that are from different physical compute nodes to communicate with each other;
  * Public: The public network is a network which OpenStack points tenant public traffic to. This requires the respective physical interface to be set as promiscuous mode. That is to say, this network needs to be mapped to a unique physical interface which is different from all other networks to avoid networking chaos. (please refer to the screenshot below)
  * Storage: Currently the storage network is not utilized by Compass. Theoretically the storage network will be used by tenants to access storage devices or services such as Swift/Cinder;

![Public network](/img/7_public_network.png)

![Promisc](/img/7_promisc.png)

