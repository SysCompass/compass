---
layout: page
title: "Overview"
description: ""
---

Compass - RESTful API Reference
===============================

Switch
------

<table border="1">
<thead>
<tr>
<th>Verb</th>
<th>URI</th>
<th>Description</th>
</tr>
</thead><tbody>
<tr>
<td>POST</td>
<td>/switches</td>
<td>Create a switch object in the system. </td>
</tr>


<tr>
<td>GET</td>
<td>/switches</td>
<td>Get switch objects in the system with given conditions, if provided. </td>
</tr>


<tr>
<td>PUT</td>
<td>/switches</td>
<td>Update switch object with new attribute values. </td>
</tr>



</tbody>
</table>

* **URL**

  _/switches_

* **Method:**

   `POST`

* **Data Params**

  A switch JSON object, with the following attributes:
   * `ip`: Management IP of the switch
   * `credentials`: SNMP or CLI credentials for the switch.


* **Success Response:**


  * **Code:** 200 <br />
    **Content:** `{ id : 12 }`


* **Error Response:**



  * **Code:** 409
    **Content:** `{ error : "Log in" }`

  OR

  * **Code:** 422 UNPROCESSABLE ENTRY <br />
    **Content:** `{ error : "Email Invalid" }`

* **Sample Call:**


Or, in the case where the credential is login and password.






