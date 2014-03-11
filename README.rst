Art 17 Consultation Tool for http://bd.eionet.europa.eu/article17/reports2012/
==============================================================================

.. contents ::

Project Name
------------
The Project Name is Article 17 Consultation.

Prerequisites - System packages
-------------------------------

These packages should be installed as superuser on.

Debian based systems
~~~~~~~~~~~~~~~~~~~~
Install this before setting up an environment::

    apt-get install python-setuptools python-dev libmysqlclient-dev libldap2-dev python-virtualenv

OS X
~~~~
Install python and pip::

    brew install python --universal --framework
    pip install virtualenv

Product directory
-----------------

Create the product directory::

    mkdir -p /var/local/art17


Install dependencies
--------------------
We should use Virtualenv for isolated environments. The following commands will
be run as an unprivileged user in the product directory.

1. Clone the repository::

    git clone git@github.com:eea/art17-consultation.git -o origin flask
    cd flask

2.1. Create & activate a virtual environment::

    virtualenv --no-site-packages sandbox
    echo '*' > sandbox/.gitignore
    source sandbox/bin/activate

2.2 Make sure setuptools >= 0.8 is installed::

    pip install -U setuptools

3. Install dependencies::

    pip install -r requirements-dev.txt

4. Create a configuration file::

    mkdir -p instance
    touch instance/settings.py

    # Check settings.local.example for configuration details

6. Set up the MySQL database::

    mysql> create database art17 CHARACTER SET utf8 COLLATE utf8_general_ci;
    ./manage.py db upgrade

7. Import sql data dump in your art17 database, see "data import" below.

8. Create your user and assign admin role to it::

    ./manage.py user create -e user_email -i user_id
    ./manage.py role create -n admin
    ./manage.py role add -u user_id -r admin
    
    
Configuration
-------------
Details about configurable settings can be found in `settings.py.example`.

Configuring the Zope API
~~~~~~~~~~~~~~~~~~~~~~~~
Some functionality (authentication and layout template) is provided by a
Zope server. Here is how to configure the app to fetch this information.

First, the Zope server needs a few scripts in its object tree. Create a
folder, for example ``art17_api``, and create `Script (Python)` objects
inside, using the files in the `zope_api` folder of this repository.

Then, add the following configuration variables to the app, using the
correct URLs for the Zope server::

    AUTH_ZOPE = True
    AUTH_ZOPE_WHOAMI_URL = 'http://zope.server.url/art17_api/whoami'
    LAYOUT_ZOPE_URL = 'http://zope.server.url/art17_api/layout'


Data Import
-----------
Initially the application's database is empty. We need to import data
from a dump (the old 2006 app's database or the new reporting data).
First we need to load this dump into a separate MySQL databse::

    mysql -e 'create database art17_2006 CHARACTER SET utf8 COLLATE utf8_general_ci;'
    mysql art17_2006 < art17_2006.sql

Then we can import this data into our app's database. Make sure to
specify the right schema version, in this case '2006'::

    ./manage.py dataset import -d import-from-2006 -i 'mysql://user:pass@localhost/art17_2006' -s 2006

An optional argument ``-f`` (fallback) exists. When there are no records to import
in a table, it copies the entire table from the specified dataset.

Build production
----------------

Setup the production environment like this (using an unprivileged user)::

    cd /var/local/art17
    # install dependencies, see above
    . sandbox/bin/activate
    cd flask
    mkdir instance
    cp settings.py.example instance/settings.py
    vim instance/settings.py

Configure database and authentication connectors, then reset the application::

    ./bin/supervisorctl reload 1>/dev/null || ./bin/supervisord


Build staging
-------------

Setup the production environment like this::

    $ cd /var/local/art17staging
    # install dependencies, see above
    . sandbox/bin/activate
    cd flask
    mkdir instance
    cp settings.py.example instance/settings.py
    vim instance/settings.py

Configure database and authentication connectors, then reset the application::

    ./bin/supervisorctl reload 1>/dev/null || ./bin/supervisord

Development hints
=================

Configure deploy
----------------

- copy ``fabfile/env.ini.example`` to ``fabfile/env.ini``
- configure staging and production settings
- run ``fab staging deploy`` or ``fab production deploy``


Running unit tests
------------------

Simply run ``py.test testsuite``, it will find and run the tests. For a
bit of speedup you can install ``pytest-xdist`` and run tests in
parallel, ``py.test testsuite -n 4``.


Contacts
========

The project owner is Søren Roug (soren.roug at eaa.europa.eu)

Other people involved in this project are:

* Cornel Nițu (cornel.nitu at eaudeweb.ro)
* Alex Eftimie (alex.eftimie at eaudeweb.ro)

Resources
=========

Hardware
--------
Minimum requirements:
 * 2048MB RAM
 * 2 CPU 1.8GHz or faster
 * 4GB hard disk space

Recommended:
 * 4096MB RAM
 * 4 CPU 2.4GHz or faster
 * 8GB hard disk space


Software
--------
Any recent Linux version.
apache2, local MySQL server


Copyright and license
=====================

This project is free software; you can redistribute it and/or modify it under
the terms of the MIT License.

More details under `LICENSE.txt`_.

.. _`LICENSE.txt`: https://github.com/eea/art17-consultation/blob/master/LICENSE.txt
