<h4>GET /adapters?name={value}</h4>


List details of all adapters or optionally filtered by an adapter name.


***Normal Response Code:*** 200

***Request parameters***

<table class="table table-bordered table-striped">
<thead><th>Name</th>
<th>Style</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>name (optional)</td>
<td>query</td>
<td>string</td>
<td>The name of the adapter</td>
</tr>

</tbody>
</table>



***Response parameters***

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
"OK" if no error occurs, or appropriate error string in case of failure
</td>
</tr>


<tr>
<td>id</td>
<td>int </td>
<td>The unique identifier of the adapter</td>
</tr>


<tr>
<td>name</td>
<td>string</td>
<td>The name of the adapter</td>
</tr>


<tr>
<td>os</td>
<td>string </td>
<td>The type of an operating system which shall be installed on the host
</td>
</tr>


<tr>
<td>target_system</td>
<td>string </td>
<td>
The type of a system which shall be installed on the host
</td>
</tr>
<tr>
<td>link</td>
<td>string </td>
<td>
The adapter link.
</td>
</tr>

</tbody>
</table>

***Sample JSON Response***


{% highlight javascript %}

{
    "status"": "OK",
    "adapters": [
        { 
            "id": 1,
            "name": "Centos_openstack",
            "os": "Centos 6.4-minimal-x86_64",
            "target_system"": "Openstack",
            "link": {
                "href": "/adapters/1",
                "rel": "self"
            }
        },
        ...
    ]
}
{% endhighlight  %}