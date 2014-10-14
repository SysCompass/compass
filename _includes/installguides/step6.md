<h2 id="step-six">Step 6 - Network</h2>



Network enables OpenStack networking configuration.
Click on "Autofill" to expand section. There are four interfaces by default, please add or delete as needed.
Please make suer you set a unique NIC for Public Network and enable the promisc mode.


![interface](/img/install/08.png)


Click "Add Subnet" on the top right side to add subnet. Please make sure you assign an external subnet to your eth1 since this interface is for Public Network.


![add subnet](/img/install/09.png)


![subnet](/img/install/10.png)


Select the start ip for each interface, it will be assigned to target machine incrementally.


![full value](/img/install/11.png)
