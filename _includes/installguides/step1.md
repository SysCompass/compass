<h2 id="step-one">Step 1 - Install Compass</h2>


Compass VM needs to have a running operating system. Compass has an automatic install script to set up itself, but currently it only supports CentOS.

Once you have installed CentOS, run <code style='background-color: #DCDCDF'>yum -y install git</code> to get git.

When git is ready, run the command:
<code style='background-color: #DCDCDF'>git clone git://git.openstack.org/stackforge/compass-core.git</code>.


![clone repository](/img/install/1_git_clone_compass.png)


Go to compass-core directory: <code style='background-color: #DCDCDF'>cd compass-core</code>
Run <code style='background-color: #DCDCDF'>./install/install.sh</code> to install compass.

![install compass](/img/install/1_run_install_script.png)


The install scripts will be asking some questions to allow users to customize their environments. 
The content bewteen parenthesis is the default setting. Press "Enter" to go with default setting.
Here we will explain those questions to make them easier to understand.

+ **Please enter the nic**

  Compass uses PXE(BOOTP) and DHCP to install OSes onto servers using network installation. This is asking you to input which nic on the Compass server you would like the DHCP service to listen on. Please note that although the default DHCP server setting listens to all interfaces on Compass server, it is recommended that you set this as the interface that is connected to the Management network.


  ![nic](/img/install/1_nic.png)


+ **Please enter the ipaddr**

  This is asking you for your server's IP address. The example value is calculated using the input from Q1. It gets the IP address of the interface you chose in Q1. In most cases, you only need to hit enter.


  ![ipaddr](/img/install/1_ipaddr.png)


+ **Please enter the netmask**

  This is self-explanatory. Please enter the netmask you have set up for management network.

  ![netmask](/img/install/1_netmask.png)


+ **Please enter the option_router**

  The option_router variable is used as the gateway for PXE to route the TFTP request traffic. The example value is calculated from Compass server's default gateway. Thus it is not always correct. It is important that you enter the gateway you have set up for your management network, because a wrong value may FAIL your future deployment.

  ![option_router](/img/install/1_option_router.png)


+ **Please enter the ip_start**

  The ip_start variable is for DHCP server to assign IPs. The ip_start and ip_end values give DHCP server an IP pool.


  ![ip_start](/img/install/1_ip_start.png)


+ **Please enter the ip_end**

  See Q5.


  ![ip_end](/img/install/1_ip_end.png)


+ **Please enter the nextserver**

  The next_server acts as the TFTP server. The example value gets it from Compass server's IP on the management interface. In most cases the example values are correct.


  ![nextserver](/img/install/1_next_server.png)


+ **Would you like to set up a local repository**

  This question cannot be answered by just hitting enter. A local repo is a repo that contains all the packages to install OpenStack. Setting up a local repo on Compass server makes the deployment much faster. Also it makes it possible to have an isolated OpenStack environment without internet access. Upon entering "y", Compass will drag the local repo from the internet and make it available to all the hosts.


  ![local repo](/img/install/1_local_repo.png)


+ **Please enter the nameserver_domains**

  This helps you setup the FQDN for Compass and its hosts.


  ![name domain](/img/install/1_domain.png)


+ **Please enter the web_source**

  This question is asking for the source code url for Compass web UI. Just hit enter, it will be downloaded.


  ![web source](/img/install/1_web_source.png)


+ **Please enter the adapters_source**

  Compass adapters are also some source code for Cobbler and Chef to use. See Q10 for instructions.


  ![adapters source](/img/install/1_adapters_source.png)


Once you answered all above questions, you can hand the installation over to Compass installation script. It will take a while to finish, depending on your location and network bandwidth.


![complete](/img/install/1_complete_installation.png)
