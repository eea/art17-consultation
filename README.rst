Art 17 Consultation Tool http://bd.eionet.europa.eu/article17/reports2012/
==========================================================================

.. contents ::

Project Name
------------
The Project Name is Article 17 Consultation.

Prerequisites - System packages
-------------------------------

These packages should be installed as superuser (root).

Debian based systems
~~~~~~~~~~~~~~~~~~~~
Install these before setting up an environment::

    apt-get install python-setuptools python-dev libmysqlclient-dev \
    libldap2-dev python-virtualenv mysql-server git


RHEL based systems
~~~~~~~~~~~~~~~~~~

Run these commands::

    yum groupinstall -y 'development tools'
    yum install -y zlib-devel bzip2-devel openssl-devel xz-libs wget

    wget http://www.python.org/ftp/python/2.7.6/Python-2.7.6.tar.xz
    xz -d Python-2.7.6.tar.xz
    tar -xvf Python-2.7.6.tar

    cd Python-2.7.6

    ./configure --prefix=/usr/local

    make
    make altinstall

    export PATH="/usr/local/bin:$PATH"

    wget --no-check-certificate \
    https://pypi.python.org/packages/source/s/setuptools/setuptools-1.4.2.tar.gz

    tar -xvf setuptools-1.4.2.tar.gz
    cd setuptools-1.4.2

    python2.7 setup.py install

    curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python2.7 -

    pip2.7 install virtualenv

    yum install mysql-server mysql git openldap-devel mysql-devel


Product directory
-----------------

Create the product directory::

    mkdir -p /var/local/art17
    mkdir /var/local/art17/logs

Create a new user::

    adduser edw

Change the product directory's owner::

    chown edw:edw /var/local/art17 -R



Install dependencies
--------------------
We should use Virtualenv for isolated environments. The following commands will
be run as an unprivileged user in the product directory::

    su edw
    cd /var/local/art17

1. Clone the repository::

    git clone https://github.com/eea/art17-consultation.git -o origin flask
    cd flask

2.1. Create & activate a virtual environment::

    virtualenv --no-site-packages sandbox
    echo '*' > sandbox/.gitignore
    source sandbox/bin/activate

2.2 Make sure setuptools >= 0.8 is installed::

    pip install -U setuptools

3. Install dependencies::

    pip install -r requirements-dep.txt

4. Create a configuration file::

    mkdir -p instance
    cp settings.py.example instance/settings.py

    # Follow instructions in instance/settings.py to adapt it to your needs.

6. Set up the MySQL database::

    # Replace [user] and [password] with your MySQL credentials and [db_name] with the name of the database:
    mysql -u[user] -p[password] -e 'create database [db_name] CHARACTER SET utf8 COLLATE utf8_general_ci;'
    ./manage.py db upgrade

7. Import sql data dump in your art17 database, see "data import" below.

8. Create your user and assign admin role to it::

    # for local user
    ./manage.py user create -e user_email -i user_id -p <password>
    # for Eionet user
    ./manage.py user create -i user_id --ldap
    # make it admin
    ./manage.py role add -u user_id -r admin


Build production
----------------

Setup the production environment like this (using an unprivileged user)::

    # install dependencies, see above
    cd /var/local/art17
    source sandbox/bin/activate

Configure supervisord and set the WSGI server port (by default it is 5000)::

    cp flask/supervisord.conf.example supervisord.conf
    vim supervisord.conf
    supervisorctl reload 1>/dev/null || ./bin/supervisord

At this stage, the application is up and running. You should also configure:

    * firewall policy
    * public webserver (see vhost.conf.example for an example)
    * start supervisord with the system (see init-svisor.example as an example
      init script)


Build staging
-------------

To setup a staging environment, follow the same steps as above. Create and use
a different database (for example ``art17staging``).

Configure supervisord and set the WSGI server port (a different one from the
production, for example 5001)::

    cd /var/local/art17staging
    source sandbox/bin/activate
    cp flask/supervisord.conf.example supervisord.conf
    vim supervisord.conf
    supervisorctl reload 1>/dev/null || ./bin/supervisord


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

Development hints
=================

Requirements
------------

User ``requirements-dev.txt`` instead of ``requirements-dep.text``::

    pip install -r requirements-dev.txt


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
the terms of the EUPL v1.1.

More details under `LICENSE.txt`_.

.. _`LICENSE.txt`: https://github.com/eea/art17-consultation/blob/master/LICENSE.txt
