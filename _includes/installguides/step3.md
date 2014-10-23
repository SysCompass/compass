<h2 id="step-three">Step 3 - Create Cluster</h2>


After you log in, you will see this page, click on "+ New Cluster" on the top right.


![home page](/img/install/3_home_page.png)


1. Cluster name: enter your cluster name

2. Target system: target system is what you would like your cluster to be. Currently we support OpenStack and OpenStack+Ceph. In this instruction, we use OpenStack Icehouse as the target system.

3. OS: The OS breeds that will be installed to the hosts. We support both CentOS-6.5 and Ubuntu-12.04.

4. Flavor: This is essentially how you fabric your cluster. There are following options:

   a. All-in-one: Choose this if you only have one server, and all components of your target system will be deployed to that server.

   b. Single-Controller, Multi-Compute. This flavor is designed specifically for OpenStack. If you have a relatively small number of servers(e.g: 2-10 servers). You may consider this option. Compass will prepare and render some environment templates into cluster deployment configurations for one controller node and multiple compute nodes. 

   c. Multinodes: Choose this option if you have a relatively larger number of servers(10+ servers). This gives a finer granularity of roles for you to assign. The concept of roles will be further discussed in later steps. Keep in mind that this flavor is designed for more advanced users who possess a deeper knowledge of the target system.



![create cluster](/img/install/3_create_cluster.png)
