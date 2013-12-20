<h4>GET /adapters/{id}/roles</h4>
Lists details of roles for the specified adapter


***Normal Response Code:*** 200

***Error Response Codes:***

  * 404 Object not found

***Request parameters***

<table class="table table-bordered table-striped">
<thead><th>Name</th>
<th>Style</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>
<tr>
<td>id</td>
<td>URI</td>
<td>int </td>
<td>The unique identifier of the adapter</td>
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
<td>"OK" if no error occurs, or appropriate error string in case of failure.
</td>
</tr>


<tr>
<td>name</td>
<td>string </td>
<td>The name of the role
</td>
</tr>


<tr>
<td>description</td>
<td>string</td>
<td>Description of the role</td>
</tr>



</tbody>
</table>




***Sample JSON Response***


{% highlight javascript %}
{
    "status": "OK",
    "roles": [
        { 
            "name": "controller",
            "description": "OpenStack controller node for the cluster"
        },
        ...
    ]
}
{% endhighlight  %}
