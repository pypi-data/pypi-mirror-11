NAME
====

    x100daemon - Make daemon for your program


SYNOPSIS
========

.. code-block::


    from x100daemon import Daemon

    pidfile = '/var/pid/hello.pid'
    d = Daemon(pidfile)
    d.daemonize()

    #your program district


DESCRIPTION
===========

    x100daemon make daemon for your program 


METHODS
=======

pidfile
---------
   Assgin your pidfile path 

daemonize
----------
    make daemon 


SUPPORTED PYTHON VERSIONS
=========================

    daemonize only supports python 3.3 or newer.


EXAMPLES
========

example
-----------

.. code-block::

    from x100daemon import Daemon

    pidfile = '/var/pid/hello.pid'
    d = Daemon(pidfile)
    d.daemonize()

    #your program district
