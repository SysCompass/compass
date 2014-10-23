<h2 id="step-ten">Step 10 - Role Assignment</h2>

*Roles* are what Compass uses to identify what each server does. In OpenStack there are controller, compute, network, storage, etc. These are all roles. When you say some node is a compute node, it means that node is running OpenStack compute services and playing the role as a compute node. We are listing all available roles on the right under "Drag to Assign". The role list is depending on the flavor you chose when you created the cluster. Different flavors may result in different granularities of roles listed in this section. Compass Appliance uses all-in-one flavor. Therefore we have one available role here called "All in One Compute". 

![roles](/img/appliance/10_role.png)

To manually assign roles, you can just drag the role and drop it at the server under "Roles" column or first select a server by checking the box next to it and click on the "Manually Assign" drop-down menu to choose roles. You can also multi-select servers and assign the same role to them.

We also can help you automatically assign roles. This would be more useful when deploying a relatively large distributed system. Click on "Auto Assign" button and you will see all available roles listed and a blank after each of them for you to input the numbers of servers you'd like to assign each role to. 

![Auto Assign](/img/appliance/10_autoassign.png)

For all-in-one role, you can just click "Assign" button and the role will be assigned to it.

![Assigned](/img/appliance/10_allinone-assigned.png)

Click on "Next" to prceed.
