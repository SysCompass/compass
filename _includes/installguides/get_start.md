<h2 id="get_start">Getting Start</h2>


To get started, we need to have an environment ready for Compass and target system. Physical machines are recommended in production environments.
For the sakes of simplicity and ease of demonstration, four virtual machines are used in this instruction:

+ One Compass VM
+ Three VMs for Compass to deploy OpenStack on.

There are some basic network requirements as well, please refer to the following image:


![compass network configuration](/img/install/Compass.png)


+ Management network in this instruction is also overlapped by Storage and Tenant network. 
+ Compass server needs to have at least two network interfaces. One connects to the internet, and the other one connects to the management network.
+ Network node(also controller and storage node, in this case) needs to have at least two interfaces, one connects to the management network and the other one connects to the external network.
+ All other nodes only need to connect to the management network.(Details about these networks will be further discussed in later steps)

The machines you are going to deploy OpenStack on need to be baremetals, even the operation system that already exists will be forcibly removed.
