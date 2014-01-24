<h4>PUT /switches/{id}</h4>

Updates the credentials of a specified switch, triggering polling switch action once update is successful.

***Normal Response Code:*** 202

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
<td>ip</td>
<td>plain</td>
<td>string</td>
<td>The switch IP address</td>
</tr>


<tr>
<td>version</td>
<td>plain</td>
<td>string </td>
<td>SNMP version when accessing the specified switch by SNMP </td>
</tr>


<tr>
<td>community</td>
<td>plain</td>
<td>string </td>
<td>SNMP community strinng when accessing the specified switch by SNMP </td>
</tr>


<tr>
<td>username</td>
<td>plain</td>
<td>string </td>
<td>SSH username when accessing the specified switch via SSH </td>
</tr>


<tr>
<td>password</td>
<td>plain</td>
<td>string </td>
<td>SSH password when accessing the specified switch via SSH </td>
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
"accepted" if the switch is created successfully, or appropriate error string in case of failure.
</td>
</tr>


<tr>
<td>state</td>
<td>string </td>
<td>Valid only if the switch is created successfully. (repolling) </td>
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



***Sample JSON Request***

{% highlight javascript %}
{
    "switch": {
        "ip": "192.168.10.2",
        "credential": {
	        "version": "2c"
        }
    }
}
{% endhighlight  %}

***Sample JSON Request***

{% highlight javascript %}
{
    "switch": {
        "ip": "192.168.10.2",
        "credential": {
            "username": "admin",
            "password": "admin"
        }
    }
}
{% endhighlight  %}

***Sample JSON Response***

{% highlight javascript %}
{
    "status": "accepted",
    "id": 1,
    "switch": {
        "state": "repolling",
        "link": {
            "href": "/switches/1",
            "rel": "self"
        }
    }
}
{% endhighlight  %}
