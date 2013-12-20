<h4>POST /clusters</h4>

Creates a cluster by user-specified name, or a UUID will be assigned automatically.

***Normal Response Code:*** 200

***Error Response Codes:***

  * 409 Duplicate key error

***Request parameters***

<table class="table table-bordered table-striped">
<thead><th>Parameters</th>
<th>Style</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>name(optional)</td>
<td>plain</td>
<td>string</td>
<td>The unique name of the cluster specified by the user, or assigned as a UUID automatically.</td>
</tr>


<tr>
<td>adapter_id</td>
<td>plain</td>
<td>int</td>
<td>The unique identifier of adapter.</td>
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
<td>id</td>
<td>int</td>
<td>The unique identifier of the cluster</td>
</tr>


<tr>
<td>name</td>
<td>string</td>
<td>The name of the cluster</td>
</tr>


<tr>
<td>link</td>
<td>dict </td>
<td>The cluster link references.</td>
</tr>

</tbody>
</table>



***Sample JSON Request***

{% highlight javascript %}
{
    "cluster": {
        "name": "",
        "adapter_id": 1
    }
}
{% endhighlight  %}

***Sample JSON Request***

{% highlight javascript %}
{
    "cluster": {
        "name": "cluster_01",
        "adapter_id": 1 
    } 
} 
{% endhighlight  %}

***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK",
    "id": 1,
    "cluster": {
        "id": 1,
        "name": "cluster_01"
        "link": {
            "href": "/clusters/1",
            "rel": "self"
        }
    }
}
{% endhighlight  %}
