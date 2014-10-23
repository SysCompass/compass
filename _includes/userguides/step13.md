<h2 id="step-thirteen">Step 13 - Deploying OpenStack</h2>

Once the deployment starts, Compass Web-UI updates the cluster progress periodically and shows them as progress bars.

![progress](/img/appliance/13_progress.png)

At this point, you will need to go back to the VirtualBox GUI and bring up the server called "allinone".

![upallinone](/img/appliance/13_up-allinone.png)

![slave_running](/img/appliance/13_slave-running.png)

Then wait for a few minutes, you should be able to see progress bar moving, which means Compass is deploying your all-in-one cluster. 
It will take approximately 15-20 minutes for your all-in-one OpenStack cluster to be deployed. Once the progress bar hits 100% and turns green, your OpenStack is up!

![Done](/img/appliance/done.png)

Now open up a new tab on the browser and go to the IP address you set for allinone server. OpenStack dashboard will show up, you can login with the credentials you set up for dashboard. If you chose to use the default values, they are:
<pre>
username: admin
password: admin
</pre>
