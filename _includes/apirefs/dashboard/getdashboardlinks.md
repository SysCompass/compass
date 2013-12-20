<h4>GET /dashboardlinks?cluster_id={cluster_id}</h4>

Lists links for dashboards of the system deployed on the specified cluster successfully

***Normal Response Code:*** 200

***Request parameters***

<table class="table table-bordered table-striped">
<thead><th>Parameters</th>
<th>Style</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>cluster_id</td>
<td>query</td>
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
<td>dashboardlinks</td>
<td>list</td>
<td>The collection of dashboard links associated with the roles of the installed 
system. Each role is as the key, and the value is the link. </td>
</tr>

</tbody>
</table>



***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK",
    "dashboardlinks": [
        {
            "os-single-controller": "http://10.12.234.3",
        },
        ...
    ]
}
{% endhighlight  %}
