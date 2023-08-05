nsxramlclient
=============

This somewhat dynamic client gets its API structure information (e.g.
URLs, paramaters, schemas, etc.) from a RAML file.

It is curently in development, more documentation in this readme will
follow soon

How to install
==============

The following install instructions will focus on Ubuntu 14.04 LTS, but
installations on other Linux distributions or on MAC should be
relatively simmilar.

Check wether pip is installed

.. code:: sh

    pip --version

If pip is not installed, install it with apt-get

.. code:: sh

    sudo apt-get update
    sudo apt-get -y install python-pip

Now you can install the nsx raml client using pip

.. code:: sh

    sudo pip install nsxramlclient --pre

If the installation fails because of missing dependencies of lxml, you
will see the following message

::

    ERROR: /bin/sh: 1: xslt-config: not found
    ** make sure the development packages of libxml2 and libxslt are installed **

In this case install the following packages through apt-get, and then
repeat the above pip installation of the nsx raml client:

.. code:: sh

    sudo apt-get install libxml2-dev libxslt-dev python-dev zlib1g-dev
