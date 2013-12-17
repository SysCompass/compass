POST /switches
--------------

Create a switch by providing a switch IP address and associated credentials.
The POST action shall trigger switch polling. During the polling process,
MAC address of the devices connected to the switch will be learned by SNMP or SSH.

*Normal Response Code:* 202

*Error Response Codes:*
  * 409 Duplicate key error
  * 400 Invalid request data

*Request parameters*

<table class="table table-bordered table-striped">
<thead><th>Name</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>ip</td>
<td>string </td>
<td>The switch IP address</td>
</tr>


<tr>
<td>version</td>
<td>string </td>
<td>SNMP version when accessing the specified switch by SNMP </td>
</tr>


<tr>
<td>community</td>
<td>string </td>
<td>SNMP community strinng when accessing the specified switch by SNMP </td>
</tr>


<tr>
<td>username</td>
<td>string </td>
<td>SSH username when accessing the specified switch via SSH </td>
</tr>


<tr>
<td>password</td>
<td>string </td>
<td>SSH password when accessing the specified switch via SSH </td>
</tr>


</tbody>
</table>



*Response parameters*

<table class="table table-bordered table-striped">
<thead><th>Name</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>status</td>
<td>string </td>
<td>
accepted if the switch is created successfully, or appropriate error string in case of failure.
</td>
</tr>


<tr>
<td>state</td>
<td>string </td>
<td>Valid only if the switch is created successfully.
Once polling switch is completed and MAC addresses retrieved,
the state of the switch shall be under_monitoring, otherwise it shall be not_reached. </td>
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



*Sample JSON Request*

{% highlight javascript %}
{
  "switch"": {
    "ip" : "192.168.10.2",
    "credential" : {
	"version": "v2c",
	"community": "public"
  }
 }
}
{% endhighlight  %}

*Sample JSON Response*


{% highlight javascript %}
{
  "status": "accepted",
  "switch": {
  "state": "not_reached",
  "link": {
 	"href": "/switches/1",
        "rel": "self"
        },
  "id": 1
  }
}
{% endhighlight  %}
