<h4>POST /clusters/{id}/action</h4>

Take actions for the specified cluster. The actions includes addHosts, removeHosts, replaceAllHosts, and deploy.
The action \"addHosts\" allows a user to add the specified machine(s) as the host(s) to the cluster.
The action \"removeHosts\" allows to remove the specified the host(s) by host ID(s) from the cluster.
The action \"replaceAllHosts\" allows to remove all existing hosts of the cluster and add new machine(s) as the new host(s) to the cluster.
The action \"deploy\" shall deploy and start to install each host(s) in the cluster.

***Normal Response Code:*** 200

***Error Response Codes:***
  * 400 Invalid usage
  * 404 Not found error
  * 409 Duplicate key error

***Request parameters***

<table class="table table-bordered table-striped">
<thead><th>Parameters</th>
<th>Style</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>id</td>
<td>URI</td>
<td>int</td>
<td>The unique identifier of the cluster</td>
</tr>


<tr>
<td><a href="#add_host_action">addHosts</a></td>
<td>plain</td>
<td>list</td>
<td>The list of machine ID(s) expected to be added as the host(s) to the cluster.</td>
</tr>

<tr>
<td><a href="#remove_host_action">removeHosts</a></td>
<td>plain</td>
<td>list</td>
<td>The list of host ID(s) expected to be removed from the cluster.</td>
</tr>

<tr>
<td><a href="#replace_hosts_action">replaceAllHosts</a></td>
<td>plain</td>
<td>list</td>
<td>The list of machine ID(s) expected to be added as the new host(s) to the cluster and replaced the existing hosts in the same cluster.</td>
</tr>

<tr>
<td><a href="#deploy_action">deploy</a></td>
<td>plain</td>
<td>list</td>
<td>The list of host IDs in the cluster expected to be deployed. Empty list means deploy all hosts in the cluster.</td>
</tr>

</tbody>
</table>

<div id="add_host_action" class="anchor_divider">
</div>

<h4 class="docs_subheader">Add hosts</h4>

**Response parameters**

<table class="table table-bordered table-striped">
<thead><th>Parameters</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>status</td>
<td>string </td>
<td>"OK" if no error occurs, or appropriate error string in case of failure.</td>
</tr>


<tr>
<td>cluster_hosts</td>
<td>list</td>
<td>The list of all hosts which is added successfully to the specified cluster.
Each host represents as a dict including the attributes "id" (host id) and "machine_id".</td>
</tr>

</tbody>
</table>



**Sample JSON Request**

{% highlight javascript %}
{
    "addHosts": [11, 12, 13]
}
{% endhighlight  %}

**Sample JSON Response**

{% highlight javascript %}
{
    "status": "OK",
    "cluster_hosts": [
        {
            "id": 1,
            "machine_id": 11
        },
        {
            "id": 2,
            "machine_id": 12
        },
        {
            "id": 3,
            "machine_id": 13
        }
    ]
}
{% endhighlight  %}

**Sample JSON Error Response**

{% highlight javascript %}
{
    "status": "Conflict Error",
    "message": --error-message--,
    "failedMachines": [12]
}
{% endhighlight  %}


<div class="anchor_divider" id="remove_host_action">
</div>

<h4 class="docs_subheader">Remove Hosts</h4>

**Response parameters**

<table class="table table-bordered table-striped">
<thead><th>Parameters</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>status</td>
<td>string </td>
<td>"OK" if no error occurs, or appropriate error string in case of failure.</td>
</tr>

<tr>
<td>cluster_hosts</td>
<td>list</td>
<td>The list of all hosts which are removed successfully from the specified cluster.
Each host represents as a dict including the attributes "id" (host id) and "machine_id".</td>
</tr>

</tbody>
</table>

**Sample JSON Request**

{% highlight javascript %}
{
    "removeHosts": [10, 20]
}
{% endhighlight  %}

**Sample JSON Response**

{% highlight javascript %}
{
    "status": "OK",
    "cluster_hosts":[
        {
            "id": 1,
            "machine_id": 10
        },
        ...
    ]
}
{% endhighlight  %}

**Sample JSON Error Response**

{% highlight javascript %}
{
    "status": "Conflict Error",
    "message": --error-message--,
    "failedMachines": [10]
}
{% endhighlight  %}


<div id="replace_hosts_action" class="anchor_divider">
</div>
<h4 class="docs_subheader">Replace hosts</h4>

**Response parameters**

<table class="table table-bordered table-striped">
<thead><th>Parameters</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>status</td>
<td>string </td>
<td>"OK" if no error occurs, or appropriate error string in case of failure.</td>
</tr>
<tr>
<td>cluster_hosts</td>
<td>list</td>
<td>The list of all hosts which successfully replaces all previous ones int the specified cluster.
Each host represents as a dict including the attributes "id" (host id) and "machine_id".</td>
</tr>

</tbody>
</table>

**Sample JSON Request**

{% highlight javascript %}
{
    "replaceAllHosts": [20, 21, 22]
}
{% endhighlight  %}

**Sample JSON Response**

{% highlight javascript %}
{
    "status": "OK",
    "cluster_hosts":[
        {
            "id": 1,
            "machine_id": 20
        },
        ...
    ]
}
{% endhighlight  %}

<div id="deploy_action" class="anchor_divider">

</div>

<h4 class="docs_subheader">Deploy</h4>

**Response parameters**

<table class="table table-bordered table-striped">
<thead><th>Parameters</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>status</td>
<td>string </td>
<td>"accepted" if no error occurs, or appropriate error string in case of failure.</td>
</tr>
<tr>
<td>deployment</td>
<td>string</td>
<td>The link of cluster installing progress</td>
</tr>

</tbody>
</table>

**Sample JSON Request**

{% highlight javascript %}
{
    "deploy": []
}
{% endhighlight  %}

**Sample JSON Request**

{% highlight javascript %}
{
    "deploy": [15]
}
{% endhighlight  %}

**Sample JSON Response**

{% highlight javascript %}
{
    "status": "accepted",
    "deployment": {
        "cluster": {
            "cluster_id": 1,
            "url": "/clusters/1/progress"
        },
        "hosts": [
            {
                "host_id": 1,
                "url": "/cluster_hosts/1/progress"
            },
            ...
        ]
    }
}
{% endhighlight  %}
