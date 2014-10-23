<h2 id="appendix1">Appendix I - Cleaning Up</h2>

If you would like to try out Compass again, you need to remove all the VirtualBox hosts and network configurations. To do so, follow the steps below:

1. Go back to VirtualBox GUI, multi-select both "compass-server" and "allinone", then right click on your mouse and select `Close -> Power Off`.

2. Multi-select both servers, then right click on your mouse and select `Remove`. There will be a pop-up window asking you for actions, click on `Delete all Files`.

3. Once you have removed all hosts, remove the host-only interface: go to `File -> Preferences`. Then click on the `Network` tab then the `Host-only Networks` tab to remove all host-only networks.

If you are using Windows, you will need local admin privilege to perform the removal of network adapters.

At this point, your Compass environment has been removed and you can start over by executing launch script again. 

