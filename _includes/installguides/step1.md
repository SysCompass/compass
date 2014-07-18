<h2 id="step-one">Step 1 - Install Compass</h2>

1. Run `git clone https://github.com/huawei-cloud/compass`.
2. Run `cd compass` to the Compass project directory.
3. Run `./install/install.sh` to setup compass environment. Please note that before you execute `install.sh`, you may setup your environment variables in `install/install.conf`, explanations and examples of those variables can be found in `install.conf`.
4. Run `source /etc/profile` to setup compass profile.
5. Run `./bin/refresh.sh` to initialize database.
6. Run `service compassd start` to start compass daemon services.
</br>
</br>

During the installation, you will be asked the following questions:

* Please enter the DHCP nic

   Select the nic you will use for the DHCP service.

* Please enter the DHCP subnet (Example: 10.145.88.0)

   Select the subnet for DHCP to distributing IP address.   

* Please enter the DHCP option_router (Example: 10.145.88.222)

   Select the router IP address for DHCP to provide optional configuration parameters to the client.

* Please enter the DHCP ip_range (Example: 10.145.88.100 10.145.88.250)

   Select a range of IP addresses for DHCP.

* Please enter the DHCP nextserver (Example: 10.145.88.222)

   Select a IP address for TFTP server where stored images and other packages for installation.


The process might take a while.
