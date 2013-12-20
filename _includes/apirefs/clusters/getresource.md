<h4>GET /clusters/{id}/{resource}</h4>

Lists resource(security, networking or partition) fpr a specified cluster

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
<td>The cluster ID</td>
</tr>


<tr>
<td>resource</td>
<td>URI</td>
<td>string</td>
<td>The name of the resource, including security, networking, and partition</td>
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
<td>resource</td>
<td>dict</td>
<td>The details of this resource</td>
</tr>
</tbody>
</table>



***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK",
    "resource": {
        "server_credentials": {
            "username": "admin",
            "password": "admin",
        },
        "service_credentials": {
            "username": "admin",
            "password": "admin"
        },
        "console_credentials":{
            "username": "admin",
            "password": "admin"
        }
    }
}
{% endhighlight  %}
