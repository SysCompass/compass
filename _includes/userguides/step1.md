<h2 id="step-one">Step 1 - Run Script</h2>

Once you have downloaded the Compass appliance zip file, extract the files on your system and open the `compass` folder and it should look like this: 


![Click launch script](/img/appliance/1_dir.png)


* If you are using Windows: run the launch.bat file

* If you are using Mac or Ubuntu, go to your compass directory, then run

   <pre style="background-color: #000000; color: #ffffff"># ./launch.sh</pre>


***Note***: If you are using Windows, during the execution, the Windows system will ask for administrator's  permission to apply changes to VirtualBox. You cannot run the launch file as administrator, it will cause problem during the following operations.

![Run Script](/img/appliance/1_runlaunch.png)

The execution may take up to 5 minutes as it imports the Compass virtual appliance image to VirtualBox depending on your hard disk I/O speed. In addtion, one virtual machine will be created by the batch script for OpenStack installation demo purposes. 

