<h2 id="step-six">Step 6 - Network</h2>



Network configurations have always been complicated when deploying distributed systems. Compass has made network configurations of OpenStack easy and intuitive.
As you can see in the image below, by default, Compass lists 4 network interfaces. 
Click on "Autofill" button and you will get a detailed view of networks. 
You can add or remove interfaces by clicking on the "+" and "-" on the right. 
Once you have the correct number of interfaces, choose one of them as your management network interface(this interface should match your network plan).
This can be done by checking the box of the interface under "is Mgmt Network" column. 
You then need to set one interface in "promisc" mode. Such interface is used for assigning external floating IPs. Do not set **promisc** and **management** on the same network interface.

![interface](/img/install/6_network.png)



Now add subnets to the interfaces by clicking on "Add Subnet" button. 
Then you can type in your subnet config. Subnets should follow the CIDR format such as *192.168.1.0/24*. You can click on "+" to add more subnets.

![auto fill](/img/install/6_auto_fill.png)


![add subnet](/img/install/6_add_subnet.png)


Once you complete creating subnets, Compass will go back to the network page. Now you need to map subnets to interfaces.
There are drop-down menus for each interface under "subnet" column. You should carefully choose the correct subnet for each interface.


![subnet](/img/install/6_full_value.png)


After mapping subnets to interfaces, you can start assigning IPs to individual servers. 
Compass-web can help you batch assign IPs. For each network interface, there is an **Autofill rule**. 
You can set a starting IP for each interface, and give an incremental rule for Compass to automatically assign IPs to all hosts on that network. You may also autofill hostnames for all servers. 
Currently we provide hostname autofill in *Host* and *Switch-IP* patterns. Click on "Fill Values" button after finishing filling in the values. You will be able to see in the bottom that all servers have been assigned with IPs and hostnames. Please make necessary changes to the servers and proceed to the next step by clicking "Next".

![full value](/img/install/6_fulled_value.png)
