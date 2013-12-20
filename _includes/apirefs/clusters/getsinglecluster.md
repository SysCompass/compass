<h4>GET /clusters/{id}</h4>

Lists details for a specified cluster

***Normal Response Code:*** 200

***Error Response Codes:***

  * 404 Not found error

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
<td>The cluster ID</td>
</tr>

</tbody>
</table>


***Response parameters***

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
<td>id</td>
<td>int</td>
<td>The unique identifier of the cluster</td>
</tr>

<tr>
<td>clusterName</td>
<td>string</td>
<td>The unique name of the cluster</td>
</tr>

<tr>
<td>link</td>
<td>string</td>
<td>The cluster reference link.</td>
</tr>
</tbody>
</table>



***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK",
    "cluster": {
        "id": 1, 
        "clusterName": "cluster_01",
        "link":{
            "href": "/clusters/1",
            "rel": "self"
        }
    }
}
{% endhighlight  %}
