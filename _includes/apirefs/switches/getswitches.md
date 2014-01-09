<h4>GET /switches?switchIp={switch_ip_address}&amp;switchIpNetwork={switch_ip_network}&amp;limit={number}</h4>
-----------------------------------------------
Queries and lists the details for the device(s) filtered by switch ID or a switch IP network, and returns a specified number of results as designated by limit.

***Normal Response Code:*** 202

***Error Response Codes:***
  * 409 Duplicate key error
  * 400 Invalid request data

***Request parameters***

<table class="table table-bordered table-striped">
<thead><th>Parameters</th>
<th>Style</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>switchIp (optional)</td>
<td>query</td>
<td>string</td>
<td>Only the switch(es) with the IP(s) will be returned. Repeating with multiple switchIp for querying multiple specified switches</td>
</tr>

<tr>
<td>
switchIpNetwork
(optional)
</td>
<td>query</td>
<td>string </td>
<td>Only the switch(es) in this network will be returned.</td>
</tr>


<tr>
<td>limit(optional)</td>
<td>query</td>
<td>int</td>
<td>Up to this number of results will be returned.</td>
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
"OK" if no error occurs, or appropriate error string in case of failure.
</td>
</tr>


<tr>
<td>state</td>
<td>string </td>
<td>The state of the specified switch. ("not_reached | under_monitoring")</td>
</tr>


<tr>
<td>id</td>
<td>int </td>
<td>The unique identifier of the switch</td>
</tr>


<tr>
<td>link</td>
<td>dict </td>
<td>The switch link references.</td>
</tr>

</tbody>
</table>

***Sample JSON Response***

{% highlight javascript %}
{
    "status": "accepted",
    "switches": [
	    {
            "ip": "192.168.10.2",
            "state": "under_monitoring",
            "link": {
                "href": "/switches/1",
                "rel": "self"
            }
        },
		....
	]
}
{% endhighlight  %}
