<h4>GET /switches/{id}</h4>

Lists details for a specified switch

***Normal Response Code:*** 200

***Error Response Codes:***

  * 404 Not found error

***Request parameters***

<table class="table table-bordered table-striped">
<thead><th>Parameters</th>
<th>Type</th>
<th>Description</th>
</thead>

<tbody>
<td>id</td>
<td>URI</td>
<td>int</td>
<td>The unique identifier of the switch</td>
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
<td>The state of the specified switch. (unreachable, notsupported, under_monitoring)</td>
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
    "status": "OK",
    "switch": {
        "ip": "192.168.10.2",
        "state": "under_monitoring",
        "link": {
            "href": "/switches/1",
            "rel": "self"
        }
    }
}
{% endhighlight  %}

***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK",
    "switch": {
        "ip": "192.168.10.2",
        "state": "unreachable",
        "link": {
            "href": "/switches/1",
            "rel": "self"
        }
    }
}
{% endhighlight  %}

***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK",
    "switch": {
        "ip": "192.168.10.2",
        "state": "notsupported",
        "link": {
            "href": "/switches/1",
            "rel": "self"
        }
    }
}
{% endhighlight  %}
