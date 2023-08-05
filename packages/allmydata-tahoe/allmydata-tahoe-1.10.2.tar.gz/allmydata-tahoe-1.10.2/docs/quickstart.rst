﻿.. -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-

==================
Getting Tahoe-LAFS
==================

Welcome to `the Tahoe-LAFS project`_, a secure, decentralized, fault-tolerant
storage system.

`about Tahoe-LAFS <about.rst>`__

.. _the Tahoe-LAFS project: https://tahoe-lafs.org

How To Get Tahoe-LAFS
=====================

This procedure has been verified to work on Windows, Mac, OpenSolaris, and
too many flavors of Linux and of BSD to list.

In Case Of Trouble
------------------

There are a few 3rd party libraries that Tahoe-LAFS depends on that might not
be easy to set up on your platform. If the following instructions don't Just
Work without any further effort on your part, then please write to `the
tahoe-dev mailing list`_ where friendly hackers will help you out.

.. _the tahoe-dev mailing list: https://tahoe-lafs.org/cgi-bin/mailman/listinfo/tahoe-dev

Install Python
--------------

Check if you already have an adequate version of Python installed by running
``python -V``. Python v2.6 (v2.6.6 or greater recommended) or Python v2.7
will work. Python v3 does not work. On Windows, we recommend the use of
native Python v2.7, not Cygwin Python. If you don't have one of these
versions of Python installed, `download`_ and install the latest version of
Python v2.7. Make sure that the path to the installation directory has no
spaces in it (e.g. on Windows, do not install Python in the "Program Files"
directory).

.. _download: https://www.python.org/downloads/

Get Tahoe-LAFS
--------------

Download the latest stable release, `Tahoe-LAFS v1.10.2`_.

.. _Tahoe-LAFS v1.10.2: https://tahoe-lafs.org/source/tahoe-lafs/releases/allmydata-tahoe-1.10.2.zip

Set Up Tahoe-LAFS
-----------------

Unpack the zip file and cd into the top-level directory.

Run "``python setup.py build``" to generate the ``tahoe`` executable in a
subdirectory of the current directory named ``bin``. This will download and
build anything you need from various websites.

On Windows, the ``build`` step might tell you to open a new Command Prompt
(or, on XP and earlier, to log out and back in again). This is needed the
first time you set up Tahoe-LAFS on a particular installation of Windows.

If you see an error like ``fatal error: Python.h: No such file or directory``
while compiling the dependencies, you need the Python development headers. If
you are on a Debian or Ubuntu system, you can install them with ``sudo
apt-get install python-dev``. On RedHat/Fedora, install ``python-devel``.

Run "``bin/tahoe --version``" (on Windows, "``bin\tahoe --version``") to
verify that the executable tool prints out the right version number after
"``allmydata-tahoe:``".

Optionally run "``python setup.py trial``" to verify that it passes all of
its self-tests.

Run Tahoe-LAFS
--------------

Now you are ready to deploy a decentralized filesystem. The ``tahoe``
executable in the ``bin`` directory can configure and launch your Tahoe-LAFS
nodes. See `<running.rst>`__ for instructions on how to do that.
