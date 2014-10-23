<h2 id="step-four">Step 4 - Discover Servers</h2>


Once you have created the cluster. You will enter a wizard. The first step on the navigation bar is "Server Selection".
Right now there should be nothing in the server table(unless you run a server discovery prior to creation of the cluster).
Compass has a mechanism to discover all the server's MAC addresses of the interfaces that are connected to a specific switch using SNMP. Click on the "Discover Servers" button to get the servers. 


![discover servers](/img/install/4_discover.png)


As you can see in the image below, Compass UI pops up a form for you to fill in your switch information. This switch should be the switch of your management network. First you need to make sure the Switch has SNMP enabled and uses standard MIBs. Compass currently supports Huawei, HP, Arista and PICA8 switches. You need to enter your Switch IP, version and Community for Compass to discover servers. The default version is "2c" and default community is "public". If you are cannot proceed with default values and having trouble getting the specific values for your switch, please consult the switch manufacturers for correct information.


![switch](/img/install/4_add_switch.png)

Once you have filled in the switch information, click add and the switch will show up on the right hand side. Select the switches from the list of switches, then click "Discover Servers".
Compass will discover all the servers that are connected to the switch ip you entered. 


![switch ip](/img/install/4_servers.png)


After a few seconds, you should be able to get a list of servers with their MAC addresses, switches they are connected to and their port numbers.
Select the servers you would like to deploy, by checking their switch IPs and port numbers based on your deployment plan. 
The search bar allows you to find the desired server quickly, and by checking the "Hide Unselected Servers" box, you can get a clearer view of the servers you have selected.
If you are unable to find server, please refer to <a href="#appendix">Appendix</a> for more information.


![discover](/img/install/4_discover_servers.png)



