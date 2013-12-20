<h4>PUT /clusterhosts/{id}/config</h4>

Updates one or more editable attributes in config for the specified host.

***Normal Response Code:*** 200

***Error Response Codes:***
  * 400 Invalid usage
  * 400 Input message error
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
<td>The unique identifier of the specified host.</td>
</tr>

<tr>
<td>hostname(optional)</td>
<td>plain</td>
<td>string</td>
<td>The name of the specified host.</td>
</tr>


<tr>
<td>networking(optional)</td>
<td>plain</td>
<td>dict</td>
<td>The networking config for the specified host</td>
</tr>

<tr>
<td>security(optional)</td>
<td>plain</td>
<td>dict</td>
<td>The security config for the specified host</td>
</tr>

<tr>
<td>partition</td>
<td>plain</td>
<td>dict</td>
<td>The partition config for the specified host</td>
</tr>

<tr>
<td>roles</td>
<td>plain</td>
<td>list</td>
<td>The roles describes the behaviors of each host in the cluster</td>
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
<td>
"OK" if no error occurs, or appropriate error string in case of failure.</td>
</tr>

</tbody>
</table>



***Sample JSON Request***

{% highlight javascript %}
{
    "hostname": "host_01",
    "networking":{
        "interfaces":{
            "management":{
                "ip": "192.168.2.100"
            }
        }
    },
    "roles": ["base"]
}
{% endhighlight  %}

***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK",
}
{% endhighlight  %}
