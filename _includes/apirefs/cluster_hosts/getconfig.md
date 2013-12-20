<h4>GET /clusterhosts/{id}/config</h4>

Lists the details of the config for the specified host.

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
<td>The unique identifier of the specified host</td>
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

<tr>
<td>hostname</td>
<td>string </td>
<td>The name of the specified host</td>
</tr>

<tr>
<td>hostid</td>
<td>int </td>
<td>The unique identifier of the host</td>
</tr>

<tr>
<td>networking(optional)</td>
<td>dict</td>
<td>The networking config for the specified host</td>
</tr>

<tr>
<td>security(optional)</td>
<td>dict</td>
<td>The security config for the specified host</td>
</tr>

<tr>
<td>partition(optional)</td>
<td>dict</td>
<td>The partition config for the specified host</td>
</tr>


</tbody>
</table>



***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK",
    "config":{
        "hostname": "host_01",
        "hostid": 1,
        "networking":{
            "interfaces":{
                "management":{
                    "ip": "192.168.2.100",
                    "mac": "28:6e:d4:47:c8:6c"
                }
            },
            "global": {
                "nameservers": "8.8.8.8",
                "search_path": "ods1;ods2;ods3",
                "gateway": "10.145.1.1",
            }
        },
        "roles: ["base"]
    }
}
{% endhighlight  %}
