<h4>GET /clusterhosts/{id}</h4>

Lists the details for the specified host.

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
<td>id</td>
<td>int </td>
<td>The unique identifier of the host</td>
</tr>

<tr>
<td>mutable</td>
<td>boolean</td>
<td>The attributes of the specified host can be modified(insert, update, delete) 
if "mutable" is True, otherwise no modification is allowed.</td>
</tr>

<tr>
<td>link</td>
<td>dict</td>
<td>The host reference link</td>
</tr>

</tbody>
</table>



***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK",
    "cluster_host":{
        "hostname": "host_01",
        "id": 1,
        "mutable": true,
        "link":{
            "href": "/clusterhosts/1",
            "rel": "self"
        }
    }
}
{% endhighlight  %}
