<h2 id="appendix1">Appendix I - Cleaning Up</h2>

If you would like to try out Compass again, you need to remove all the VirtualBox hosts and network configurations. To do so, follow the steps below:

1. Go back to VirtualBox GUI, multi-select both "compass-server" and "allinone", then right click on your mouse and select `Close -> Power Off`.

   ![cleanup](/img/appliance/cleanup1.png)

   ![cleanup1](/img/appliance/cleanup2.png)

2. Multi-select both servers, then right click on your mouse and select `Remove`.

   ![select both](/img/appliance/select_both_and_remove.png)

   There will be a pop-up window asking you for actions, click on `Delete all Files`.

   ![delete all files](/img/appliance/deleteallfiles.png)

3. Once you have removed all hosts, remove the host-only interface: go to `File -> Preferences`. 

   ![preferences](/img/appliance/preference.png)

   Then click on the `Network` tab then the `Host-only Networks` tab to remove all host-only networks.

   ![network](/img/appliance/network.png)

   ![remove](/img/appliance/remove.png)

   ![cleaned_network](/img/appliance/cleaned-networks.png)

If you are using Windows, you will need local admin privilege to perform the removal of network adapters.

![clean all](/img/appliance/cleaned-all.png)

At this point, your Compass environment has been removed and you can start over by executing launch script again. 

