<h4>GET /clusters</h4>

Lists details for all clusters

***Normal Response Code:*** 200

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
    "clusters": [
        {
            "id": 1, 
            "clusterName": "cluster_01",
            "link":{
                "href": "/clusters/1",
                "rel": "self"
            }
        },
        ...
    ]
}
{% endhighlight  %}
