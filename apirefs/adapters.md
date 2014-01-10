---
layout: page
title: "Documentation"
tag_li: "adapter"
description: ""
apis:
  - switch.md
  - machine.md
---

{% include JB/setup %}



{% capture subhead %}
  <h1>API Reference</h1>
  <p class="lead">Reference Documentation of Compass RESTful API</p>
{% endcapture %}


{% capture maincontent %}

{% include apirefs/links.md %}

<h3>Adapter Methods</h3>

<table class="table table-stripped">
<thead>
<th>Method</th>
<th>URI</th>
<th>Description</th>
<th></th>
</thead>

<tr>
<td><span class="label label-success">GET</span></td>
<td>/adapters?name=value</td>
<td>Lists details of all adapters, optionally filtered by an adapter name </td>
<td><button type="button" class="btn btn-sm btn-primary" data-target="#adapters_query"
 data-toggle="collapse">Detail</button></td>
</tr>
<tr>
<td colspan="4" class="hiddenRow">
<div class="accordian-body collapse" id="adapters_query">
 {% capture myinclude %}{% include apirefs/adapters/query_get.md %}{% endcapture %}
{{ myinclude | markdownify }}
</div>
</td>
</tr>

<tr>
<td><span class="label label-success">GET</span></td>
<td>/adapters/{id}</td>
<td>
Lists details for a specified adapter.
</td>
<td><button type="button" class="btn btn-sm btn-primary"
data-target="#adapters_get" data-toggle="collapse">Detail</button></td>
</tr>
<tr>
<td colspan="4" class="hiddenRow">
<div class="accordian-body collapse" id="adapters_get">
 {% capture myinclude %}{%  include apirefs/adapters/get.md %}{% endcapture %}
{{ myinclude | markdownify }}
</div>
</td>
</tr>



<tr>
<td><span class="label label-success">GET</span></td>
<td>/adapters/{id}/roles</td>
<td>Lists role details for a specified adapter
</td>
<td><button type="button" class="btn btn-sm btn-primary"
 data-target="#adapters_role"
 data-toggle="collapse">Detail</button></td>
</tr>
<tr>
<td colspan="4" class="hiddenRow">
<div class="accordian-body collapse" id="adapters_role">
 {% capture myinclude %}{%  include apirefs/adapters/get_roles.md %}{% endcapture %}
{{ myinclude | markdownify }}
</div>
</td>
</tr>

</table>

{% endcapture %}

{% include /apirefs/template.html %}
