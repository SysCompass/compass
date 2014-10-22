<h2 id="step-nine">Step 9 - Role Assignment</h2>


In this step, you will be assigning roles to the servers. As we have discussed in earlier steps, roles of a server are essentially describing what that server does. Depending on the flavor you chose, roles will be appearing in different granularities. In this instruction, we are using "Single Controller, Multiple Compute" flavor, which gives us a few basic roles, such as:  Controller, Compute node, Network node and storage node. If you chose to use "multi-node" flavor, you will get more detailed roles such as: queue node, database node and so on.
Here are some explanations on nodes we used for this instruction:


+ Controller nodes are responsible for running the management software services needed for the OpenStack environment to function.
+ Compute nodes run the virtual machine instances in OpenStack.
+ Storage nodes store all the data required for the environment, including disk images in the Image Service library, and the persistent storage volumes created by the Block Storage service. 
+ Network nodes are responsible for doing all the virtual networking needed for people to create public or private networks and uplink their virtual machines into external networks.


For auto assign, enter the number of each nodes that you would like to assign, then click "Assign".


![role](/img/install/9_auto_assign.png)


For manually assign, drag a specific role and drop it at the desired server.


![assignment](/img/install/9_drag_assign.png)


Click "Next" when you are satisfied with role assignment.
