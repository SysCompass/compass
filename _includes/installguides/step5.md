<h2 id="step-five">Step 5 - OS Global Config</h2>



In this step you are going to tell Compass what OS configuration you would like to have on your servers. Most of them are self-explanatory, some of them have been pre-filled. But the following items should be dealt with carefully:

**NTP Server**: Compass manages NTP service. You can fill in Compass server IP here. Or if you have existing NTP servers in your cluster/data center. You can fill one of them here.

**DNS Servers**: Same as NTP server, if you do not have an existing DNS server, Compass also takes care of DNS service. You can fill in Compass server IP here.	

**Local Repository**: This is the repository for Compass to drag packages during the deployment. If you have pre-setup the repository somewhere reachable in your cluster or you chose 'y' when Compass install script asked you if you would like to setup a local repository, you may fill in the value here. Local repo behavior will be enabled in a global scope once a value is set in this step. 



![os global config](/img/install/5_config.png)

When you have filled in all the required fields, click "Next" and it will bring you to the network step.
