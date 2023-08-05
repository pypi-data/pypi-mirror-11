.. contents::

Introduction
============

See the doc of http://pypi.python.org/pypi/five.z2monitor


Use zc.monitor and additional plugins to fetch probes via another thread than the one defined in Zope.

Once the instance is running zc.monitor thread listen to another port (127.0.0.1:8888 in this buildout). You can query values using simple python script or nc.

Example:

  echo 'uptime' | nc -i 1 localhost 8888


Or (when instance is up):

    bin/instance monitor stats


Probes
======

Currently supported probes:

- cache_size -- cache sizes informations
- conflictcount -- number of all conflict errors since startup
- dbactivity -- number of load, store and connections on database (default=main) for the last x minutes (default=5)
- dbinfo [main] -- Get database statistics (number of database loads, number of database stores, number of connections, number of active/inactive objects in all object caches, number of active objects in the object caches)
- dbsize -- size of the database (default=main) in bytes
- errorcount -- number of error present in error_log (default in the root).
- help -- Get help about server commands
- monitor -- Get general process info (number of opened database connections, virtual memory size, resident memory size)
- objectcount -- number of objects in the database (default=main)
- refcount -- the total amount of object reference counts
- requestqueue_size -- number of requests waiting in the queue to be handled by zope threads
- stats -- Stats of all information Products.ZNagios know
- threads -- Dump current threads execution stack
- unresolved_conflictcount -- number of all unresolved conflict errors since startup
- uptime -- uptime of the zope instance in seconds
- zeocache -- Get ZEO client cache statistics
- zeostatus -- Get ZEO client status information


How it works
============

This package use differents package

- five.z2monitor:
- Products.ZNagios: 
- munin.zope:
- zc.z3monitor:
- zc.monitorcache:
- zc.monitorlogstats:
- ztfy.monitor:


Add lines on your buildout::

    <product-config five.z2monitor>
        bind 127.0.0.1:8888
    </product-config>

