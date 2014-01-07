<h2 id="step-five">Step 5 - Discover Machines</h2>

This page enables the hardware discovery mechanism. Enter switch IP addresses and their credentials, Compass will return all the machines that are connected to those switches. Because of the golden image does not have a real switch in its environment, we play a little trick here for demo purposes only: in the Switch IP field, type in “127.0.0.1”. Compass will recognize this particular IP address and return two machines that are previously created by the batch file. The default “SNMP version” and “Community” are “v2c” and “public”, respectively.

![Find servers](/img/5_discover_machines.png)

By clicking “Find Servers”, you will see:

![Select servers](/img/5_select_servers.png)

Compass lists all the machines it has discovered on the right hand side of the server page. A machine(server) instance has four attributes: MAC address, Switch IP address, VLAN ID and Port number. You can see two discovered machines in the screenshot above. Those machines are preconfigured for demo purposes only. Click on “Continue” to proceed.

