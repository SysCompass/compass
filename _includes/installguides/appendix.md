<h2 id="appendix">Appendix - Frequently Asked Questions</h2>



**Q: After I filled in the switch information and clicked on find servers, nothing showed up. Why?**

**A:** They may be various reasons that cause this issue. 

Fisrt, the reason might be switch MAC address aging. you need to make sure if the servers you wish to install are still actively sending data to their uplink. If those servers have been halted or shutdown for a while, switches are aging their MAC-address tables periodically. You need to restart those servers to have them send signals to their uplinks. 

If it still does not work. You might have to head down to the lab(if physical servers) to check the physical connections and health of those servers as well.

**Q: Some errors occurred but I do not seem to understand, where can I see the logs?**

**A:** Please login to your Compass server and go to /var/log/compass/ directory for service logs.

**Q: The installation of Compass server seems to take a long time as well as occasionally get stuck at some point, how to resolve this?**

**A:** All our mirrors and package resources are based in North America. If you are running this script on servers based in Asia or Europe, it is very common to take a long time to download packages. We will be working on better content delivery solutions in the next phase. Sometimes if the script is installing pip dependencies, it may look like the whole progress hangs, it is a known issue for pip and it will succeed eventually.

**Q: I click "deploy", there is still no progress after waited for a while. Why?**

**A:** You will need to restart all the target servers, only by restarting hosts PXE can be triggered.

**Q: I would like to delete a cluster that I create previously, but I do not find any delete button, how can I do this?**

**A:** Currently there is not a cluster delete button on the web UI. But you may follow the steps below to delete a cluster:

+ Login to your compass server.

+ Run <code style='background-color: #DCDCDF'>. ~/.virtualenvs/compass-core/bin/activate</code> to set up the virtual environment.

+ Go to compass-core directory and run <code style='background-color: #DCDCDF'>./bin/refresh.sh</code> to clean database and restart services.

  As you can see from the image below, it will recommend you to run several commands to do the specifically clean. Run the commands as needed.

  ![refresh](/img/install/a_refresh.png)

**Q: I tried to deploy on Ubuntu, when I started deploy, I occured this error on my target machine. How to fix it?**
![network error](/img/install/ubuntu_network.png)

**A:** That may be caused by interfaces disorder, which means the mac address the interface connected to does not match the mac address of the target machine.
To avoid that problem, make sure every NIC uses the same adapter. 

**Q: I tried to deploy on Ubuntu, after I click the "Deploy" buttom, I restart my target machine, the progress still does not start.**

**A:** Entry into BIOS setup screen, check "Boot" tap, make sure the network lists on the top, then exit. 
 
