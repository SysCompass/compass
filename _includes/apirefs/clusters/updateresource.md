<h4>PUT /clusters/{id}/{resource}</h4>

Updates the configuration information of the specified cluster. The configuration includes Security config, Networking config, and Partition config.

***Normal Response Code:*** 200

***Error Response Codes:***
  * 400 Invalid usage
  * 404 Not found error
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
<td>id</td>
<td>URI</td>
<td>int</td>
<td>The unique identifier of the cluster</td>
</tr>


<tr>
<td>resource</td>
<td>URI</td>
<td>string</td>
<td>The name of the resource, including <a href="#cluster_resource_security">security</a>,
<a href="#cluster_resource_networking">networking</a>, and <a href="#cluster_resource_partition">partition</a></td>

</tr>

</tbody>
</table>

<div id="cluster_resource_security" class="anchor_divider">
</div>

<h4 class="docs_subheader">Security</h4>

***Request parameters***

<table class="table table-bordered table-striped">
<thead><th>Parameters</th>
<th>Style</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>username</td>
<td>plain</td>
<td>string</td>
<td>User specified username for credentials in security config</td>
</tr>


<tr>
<td>password</td>
<td>plain</td>
<td>string</td>
<td>User specified password for credentials in security config</td>
</tr>

<tr>
<td>server_credentials</td>
<td>plain</td>
<td>dict</td>
<td>The credentials for accessing the host after the installation completes.</td>
</tr>

<tr>
<td>service_credentials</td>
<td>plain</td>
<td>dict</td>
<td>The credentials for services deployed to the cluster. The credentials are the same for all services.</td>
</tr>

<tr>
<td>console_credentials</td>
<td>plain</td>
<td>string</td>
<td>The credentials for accessing the system deployed to the cluster.</td>
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

</tbody>
</table>

***Sample JSON Request***

{% highlight javascript %}
{
    "security": {
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

***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK"
}
{% endhighlight  %}


<div id="cluster_resource_networking" class="anchor_divider">
</div>
<h4 class="docs_subheader">Networking</h4>

***Request parameters***

<table class="table table-bordered table-striped">
<thead><th>Parameters</th>
<th>Style</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>ip_start</td>
<td>plain</td>
<td>string</td>
<td>The start IP address of the IP range</td>
</tr>


<tr>
<td>ip_end</td>
<td>plain</td>
<td>string</td>
<td>The end IP address of the IP range</td>
</tr>

<tr>
<td>netmask</td>
<td>plain</td>
<td>string</td>
<td>The netmask of all IP addresses in the IP range.</td>
</tr>

<tr>
<td>gateway(optional)</td>
<td>plain</td>
<td>string</td>
<td>The gateway of all IP addresses in the IP range</td>
</tr>

<tr>
<td>vlan</td>
<td>plain</td>
<td>int</td>
<td>The Vlan ID, which all IP addresses in the IP range belongs to.</td>
</tr>


<tr>
<td>nic</td>
<td>plain</td>
<td>string</td>
<td>The name of the network adapter.</td>
</tr>

<tr>
<td>nameservers</td>
<td>plain</td>
<td>string</td>
<td>The IP address of the nameservers for global config.</td>
</tr>

<tr>
<td>search_path</td>
<td>plain</td>
<td>string</td>
<td>The search path of DNS for global config.</td>
</tr>

<tr>
<td>gateway</td>
<td>plain</td>
<td>string</td>
<td>The gateway for global networking config</td>
</tr>

<tr>
<td>proxy(optional)</td>
<td>plain</td>
<td>string</td>
<td>The proxy for global networking config.</td>
</tr>

<tr>
<td>ntp-server</td>
<td>plain</td>
<td>string</td>
<td>The ntp server for global networking config</td>
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

</tbody>
</table>

***Sample JSON Request***

{% highlight javascript %}
{
    "networking": {
        "interfaces":{
            "management": {
                "ip_start": "10.120.8.100",
                "ip_end": "10.120.8.200",
                "netmask": "255.255.255.0",
                "gateway": "",
                "vlan": "",
                "nic": "eth0"
            },
            "tenant": {
                "ip_start": "192.168.10.100",
                "ip_end": "192.168.10.200",
                "netmask": "255.255.255.0",
                "gateway": "",
                "vlan": "",
                "nic": "eth2"
            },
            "public":{
                "ip_start": "12.145.68.100",
                "ip_end": "12.145.68.200",
                "netmask": "255.255.255.0",
                "gateway": "",
                "vlan": "",
                "nic": "eth3"
            },
            "storage":{
                "ip_start": "172.29.8.100",
                "ip_end": "172.29.8.200",
                "netmask": "255.255.255.0",
                "gateway": "",
                "vlan": "",
                "nic": "eth4"
            }
        },
        "global":{
            "nameserver": "8.8.8.8",
            "search_path": "ods1;ods2;ods3",
            "gateway": "10.145.1.1",
            "proxy": "",
            "ntp_server": ""
        }
    }
}
{% endhighlight  %}

***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK"
}
{% endhighlight  %}

<div id="cluster_resource_partition" class="anchor_divider">
</div>
<h4 class="docs_subheader">Partition</h4>

***Request parameters***

<table class="table table-bordered table-striped">
<thead><th>Parameters</th>
<th>Style</th>
<th>Type</th>
<th>Description</th>

</thead>

<tbody>

<tr>
<td>partition</td>
<td>plain</td>
<td>string</td>
<td>The partition config for the excepted host to install</td>
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

</tbody>
</table>

***Sample JSON Request***

{% highlight javascript %}
{
    "partition": "/home 20%;"
}
{% endhighlight  %}

***Sample JSON Response***

{% highlight javascript %}
{
    "status": "OK"
}
{% endhighlight  %}
