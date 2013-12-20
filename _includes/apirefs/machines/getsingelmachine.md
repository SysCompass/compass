<h4>GET /machines/{id}</h4>

Lists the details for a specified machine.

***Normal Response Code:*** 200

***Error Response Codes:***

  * 404 Not found error

**Request parameters**

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
<td>The unique identifier of the machine</td>
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
<td>switch_ip</td>
<td>string </td>
<td>The IP address of the switch which queried machine(s) connects to</td>
</tr>

<tr>
<td>mac</td>
<td>string </td>
<td>The MAC address of the machine</td>
</tr>

<tr>
<td>vlan</td>
<td>int</td>
<td>The machine Vlan ID</td>
</tr>

<tr>
<td>port</td>
<td>int</td>
<td>The port number of the machine</td>
</tr>

<tr>
<td>id</td>
<td>int </td>
<td>The unique identifier of the machine</td>
</tr>


<tr>
<td>link</td>
<td>dict </td>
<td>The machine link references.</td>
</tr>

</tbody>
</table>

***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK",
    "machine": {
        "mac": "28:6e:d4:47:c8:6c",
        "vlan": 1,
        "port": 10,
        "id": 1,
        "switch_ip": "172.29.8.40",
        "link": {
            "href": "/machines/1",
            "rel": "self"
        }
    }
}
{% endhighlight  %}
