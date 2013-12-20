<h4>GET /clusters/{id}/progress</h4>

Lists progress details for a specified cluster

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
<td>The cluster ID</td>
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
<td>state</td>
<td>string</td>
<td>The state describes the step of the installing for the specified cluster</td>
</tr>

<tr>
<td>percentage</td>
<td>float</td>
<td>The percentage of the installing progress for the specified cluster</td>
</tr>

<tr>
<td>messages</td>
<td>list</td>
<td>The messages are generated during the installation of all hosts in the specified cluster</td>
</tr>

<tr>
<td>severity</td>
<td>string</td>
<td>The severity of the installing message</td>
</tr>

</tbody>
</table>



***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK",
    "progress": {
        "id": 1,
        "state": "INSTALLING
        "percentage": 0.3,
        "messages": [
            "Configuring Net Management",
            ...
        ],
        "severity": "INFO"
    }
}
{% endhighlight  %}
