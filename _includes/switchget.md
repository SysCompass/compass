GET /switches?name=value
------------------------
Queries and lists the details for the device(s) filtered by switch ID or a switch IP network, and returns a specified number of results as designated by limit.



Create a switch by providing a switch IP address and associated credentials. The POST action shall trigger switch polling. During the polling process, MAC address of the devices connected to the switch will be learned by SNMP or SSH.

*Normal Response Code:* 202

*Error Response Codes:*
  * 409 Duplicate key error
  * 400 Invalid request data

*Request parameters*

