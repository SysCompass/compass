<h2 id="step-ten">Step 10 - Role Assignment</h2>

*Roles* are what Compass uses to identify what each server does. In OpenStack there are controller, compute, network, storage, etc. These are all roles. When you say some node is a compute node, it means that node is running OpenStack compute services and playing the role as a compute node. We are listing all available roles on the right under "Drag to Assign". The role list is depending on the flavor you chose when you created the cluster. Different flavors may result in different granularities of roles listed in this section. Compass Appliance uses all-in-one flavor. Therefore we have one available role here called "All in One Compute". 

![roles](/img/appliance/10_role.png)

To manually assign roles, you can just drag the role and drop it at the server under "Roles" column.


![Assigned](/img/appliance/10_allinone-assigned.png)

Click on "Next" to prceed.
