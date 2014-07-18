<h2 id="appendix2">Appendix II - Frequently Asked Questions</h2>



**Q: During the Compass installation, I stuck at `Finished processing dependencies for pip==1.2.1` for a while, dose the installation complete or do I need to do something to continue?**

**A:** The installation has not completed, it will take a couple of minutes to continue, so you do not have to do anything.

**Q: In the console I got an error "Operating system not found", then the whole process stoped.**

**A:** There a several possible reasons:
 * IP-start and IP-end address is different.
 * host name is already existed.
 * IP address is duplicated.


To fix the problem, run `/opt/compass/bin/refresh.sh` to refresh the database, `service compassd restart`, `service httpd restart` to restart compass web service.
 
