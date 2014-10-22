<h2 id="step-five">Step 5 - Discover Machines</h2>

You will see a block coming up at the left hand side. This block is for you to enter the switch information.

This step allows you to discover hardware information. Enter switch IP addresses and their credentials, Compass will return all the machines that are connected to those switches. Because the Compass appliance does not have a real networking switch in its environment, we mock a switch functinality for demo purposes only: in the Switch IP field, type in “33.33.33.10”. Compass will recognize this particular IP address and return the machine that is previously created by the script file. The default “SNMP version” and “Community” are “v2c” and “public”, respectively.

![Add Switch](/img/appliance/5_addswitch.png)

<br />
<br />
By clicking “Add”, you will see on the right hand side that "33.33.33.10" has been added:

![Discover](/img/appliance/5_discover.png)

Click on "Discover". It will take no more than 3 seconds to load the default machine information specifically for Compass Appliance.

![Server](/img/appliance/5_selectserver.png)

A machine with a MAC address of "00:01:02:03:04:05" will be added at the bottom of this page. Check the box on its left and click "Next".
