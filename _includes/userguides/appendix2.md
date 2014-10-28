<h2 id="appendix2">Appendix II - Frequently Asked Questions</h2>
**Q: When I go to the Compass server url, browser does not seem to respond. Why? **

**A:** There are a few possible reasons:

I. If you are using Wnidows, your VirtualBox HostOnly Network Adapter may be misconfigured

* Go to Virtualbox UI 
* Check the network adapter setting by `File -> Preference`

* Then click on the `Network` tab and choose the host-only adapter used by compass-servre VM, which is the Adapter 2 of compass-server. For example, in our case, it is `Host-only Networks -> VirtualBox Host-Only Ethernet Adapter #2`

* If the `IPv4 Address` field is not set as `33.33.33.10`, you can run the `fix_adapter` batch file under the `compass-server` folder. The issue is caused by Windows as it changes network adapter addresses to `169.254` subnet at times.

II. Compass VM powerd off

Go to VirtualBox UI and check if the VM `compass-server` is powerd on.


III. Compass Apache2 server is not running

* Open up an ssh session and connect to `ssh://33.33.33.20:22`,
or login in the VM console of `compass-server` on VirtualBox
* The default username and password for compass server are: `root/P@ssw0rd`
* Check the apache server by running 

  <pre style="background-color: #000000; color: #ffffff"># service httpd status</pre>

  and see if it's running
* If apache server is not running, start it by running 

  <pre style="background-color: #000000; color: #ffffff"># service httpd start</pre>


**Q: If I wanted to retry compass after one successful deployment, would I have to clean up and run the script again?**

**A: **Technically yes. But there is a way to work around. You can simply log on to the compass server(`33.33.33.20`), activate the compass virtual environment by running 

  <pre style="background-color: #000000; color: #ffffff"># . ~/.virtualenvs/compass-core/bin/activate</pre>

  and then run 

  <pre style="background-color: #000000; color: #ffffff"># /opt/compass/bin/refresh.sh</pre>

   from where you would power off `allinone` vm, go back to the UI start point and try Compass again.

**Q: The deployment is taking forever. Is it unattended? Do I have to wait by my computer during the deployment?**

**A:** Yes it is unattended an no you don't have to wait (feel free to grab your lunch and come back)

**Q: During the installation, the following problem occurs to me. How can I continue?**

![centos](/img/appliance/faqcentos.png)

**A:** This is not a fatal problem, it may happen to mac, just press "OK" to continue.

