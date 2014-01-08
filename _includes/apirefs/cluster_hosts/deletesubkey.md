<h4>DELETE /clusterhosts/{id}/config/{sub_key}</h4>

Lists the details of the config for the specified host.

***Normal Response Code:*** 200

***Error Response Codes:***
  * 400 Invalid usage
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
<td>The unique identifier for the specified host</td>
</tr>

<tr>
<td>sub_key</td>
<td>URI</td>
<td>string</td>
<td>One of the attributes in config for the specified host. Only supports the arributes "ip" and "roles" in the config to be deleted </td>
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

***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK"
}
{% endhighlight  %}
