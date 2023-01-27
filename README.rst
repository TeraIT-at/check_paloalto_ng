=============================================
check_paloalto_ng: a Nagios/Icinga Plugin
=============================================
check_paloalto_ng is a **Nagios/Icinga plugin** for Palo Alto Next Generation Firewalls, that was initially developed by ralpha089 (https://github.com/ralph089/nagios_check_paloalto)
It is written in Python and based on the PA REST API.


Tested on:

- PA-500 v6.0.1 - v6.0.9
- PA-3050 v6.0.9 - 7.1.9


Documentation
-------------
https://check-paloalto-ng.readthedocs.io/en/latest/

Quickstart
----------
Please make sure you have python-dev and libxslt1-dev installed on your machine.

To install check_paloalto_ng::

	$ pip install check_paloalto_ng --upgrade

or use::

	$ pip3 install check_paloalto_ng --upgrade

The plugin requires a token to get information from the PA-REST-API. Please see the following link for more information:
https://check-paloalto-ng.readthedocs.io/en/latest//configuration.html#token

Usage
-----
Command-line usage::

    usage: check_paloalto [-h] -H HOST -T TOKEN [-v] [-t TIMEOUT] [--reset]
                      [--version]
                      {diskspace,certificates,licenses,load,useragent,environmental,powersupply,pppoe,sessinfo,thermal,throughput,interface,cluster,antivirus,threat,bgp,qos,reports}
                      ...

    positional arguments:
      {diskspace,certificates,licenses,load,useragent,environmental,powersupply,pppoe,sessinfo,thermal,throughput,interface,cluster,antivirus,threat,bgp,qos,reports}
        diskspace           check used diskspace.
        certificates        check the certificate store for expiring certificates: Outputs is a warning, if a certificate is in range.
        licenses            check the licenses for expiring licenses: Outputs is a warning, if a license is in range.
        load                check the CPU load.
        useragent           check for running useragents.
        environmental       check if an alarm is found.
        powersupply         check present power supplies.
        pppoe               check the pppoe interface.
        sessinfo            check important session parameters.
        thermal             check the temperature.
        throughput          check the throughput.
        interface           check the interfaces. If none specified will check all.
        cluster             check the cluster status.
        antivirus           check antivirus informations.
        threat              check threat informations.
        bgp                 check bgp informations.
        qos                 check quality of service.
        reports             get reports values

    optional arguments:
      -h, --help            show this help message and exit

    Connection:
      -H HOST, --host HOST  PaloAlto Server Hostname
      -T TOKEN, --token TOKEN
                            Generated Token for REST-API access

    Debug:
      -v, --verbose         increase output verbosity (use up to 3 times)
      -t TIMEOUT, --timeout TIMEOUT
                            abort check execution after so many seconds (use 0 for
                            no timeout)
      --reset               Deletes the cookie file for the throughput check.

    Info:
      --version             show program's version number and exit

