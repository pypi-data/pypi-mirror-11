
SNMP Proxy Forwarder
--------------------

This tool works as an application-level proxy with a built-in SNMP
message router. It can listen for SNMPv1/v2c/v3 messages on one interface,
parse them to choose their ultimate destinations, and finally send them
out through possibly another interface.

Typical use for an SNMP proxy is to work as an application-level firewall
or a protocol translator that enables SNMPv3 access to a SNMPv1/SNMPv2c
entity or vice versa.

Installation
------------

The easiest way to download and install SNMP Proxy and its dependencies
is to use easy install:

$ pip install snmpfwd

or

$ easy_install snmpfwd

Alternatively, you can download SNMP Proxy from SourceForge download servers:

https://sourceforge.net/projects/snmpfwd

Then you can either install the scripts with standard 

$ python setup.py install

or simply run them off your home directory (make sure to install dependencies).

Getting help
------------

If something does not work as expected, please try browsing snmpfwd
mailing list archives:

http://lists.sourceforge.net/mailman/listinfo/snmpfwd-users

or post your question to <snmpfwd-users@lists.sourceforge.net>

Feedback
--------

I'm interested in bug reports and fixes, suggestions and improvements.

---
Written by Ilya Etingof <ilya@snmplabs.com>, 2014-2015
