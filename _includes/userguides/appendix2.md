<h2 id="appendix2">Appendix II - Frequently Asked Questions</h2>
**Q: When I go to [http://33.33.33.10/ods/ods.html?config=demo](http://33.33.33.33.10/ods/ods.html?config=demo), the browser does not seem to respond. Why? **

**A:** There are a few possible reasons:

I. VirtualBox HostOnly Network Adapter is misconfigured

* Go to Virtualbox UI 
* Check the network adapter setting by `File -> Preference`
![wrong_net_2_1](/img/faq_wrong-net2-1.png)

* Then click on the `Network` tab and choose the host-only adapter used by CompassDemo VM, which is the Adapter 2 of the CompassDemo system. For example, in our case, it is `Host-only Networks -> VirtualBox Host-Only Ethernet Adapter #2`
![wrong_net_2_2](/img/faq_wrong-net2-2.png)

* If the `IPv4 Address` field is not set as `33.33.33.1`, you can run the `fix_adapter` batch file under the `compass` folder. The issue is caused by Windows as it changes network adapter addresses to `169.254` subnet at times.

II. Compass VM powerd off

Go to VirtualBox UI and check if the VM `CompassDemo` is powerd on.

![not_powerd_on](/img/faq_notpoweredon.png)


III. Compass Apache2 server is not running

* Open up an ssh session and connect to `ssh://33.33.33.10:22`,
or login in the VM console of `CompassDemo` on VirtualBox
* The default username and password for compass server are: `root/huawei`
* Check the apache server by running `service httpd status` and see if it's running
* If apache server is not running, start it by running `service httpd start`


**Q: If I wanted to retry compass after one successful deployment, would I have to clean up and run the script again?**

**A: **Technically yes. But there is a way to work around. You can simply log on to the compass server(`33.33.33.10`) and run `/opt/compass/bin/refresh.sh`, from where you would power off those two hosts, go back to the UI start point and try Compass again.

**Q: The deployment is taking forever. Is it unattended? Do I have to wait by my computer during the deployment?**

**A:** Yes it is unattended an no you don't have to wait (feel free to grab your lunch and come back)

