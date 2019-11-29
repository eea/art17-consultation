Art 17 Consultation Tool
=========================
https://nature-art17.eionet.europa.eu/article17/reports2012

|travis| |docker|

.. |travis| image:: https://travis-ci.org/eea/art17-consultation.svg?branch=master 
   :target: https://travis-ci.org/eea/art17-consultation
.. |docker| image:: https://img.shields.io/docker/build/eeacms/art17-consultation
   :target: https://hub.docker.com/r/eeacms/art17-consultation/

.. contents ::

Prerequisites
=============

1. Install `Docker`_

.. _`Docker`: https://docs.docker.com/engine/installation/
2. Install `Docker Compose`_

.. _`Docker Compose`: https://docs.docker.com/compose/install/

Installing the application
==========================

1. Get the source code::

        $ git clone https://github.com/eea/art17-consultation.git
        $ cd art17-consultation

2. Customize env files::

        $ cp docker/app.env.example docker/app.env
        $ cp docker/db.env.example docker/db.env

3. Customize docker orchestration::

        $ cp docker-compose.override.yml.example docker-compose.override.yml

4. Start stack, all services should be "Up" ::

        $ docker-compose up -d
        $ docker-compose ps

* Create your user and assign admin role to it::

        # for local user
        ./manage.py user create -e user_email -i user_id -p <password>
        # for Eionet user
        ./manage.py user create -i user_id --ldap
        # make it admin
        ./manage.py role add -u user_id -r admin

Configuration
-------------
Details about configurable settings can be found in `settings.py.example`.

Configuring the LDAP SERVER
~~~~~~~~~~~~~~~~~~~~~~~~
The authentication is provided by a LDAP SERVER.
Add the following configuration variables to the app, using the
correct URLs for the LDAP server:

    EEA_LDAP_SERVER=ldaps://ldap.example.com
    EEA_LDAP_PORT=389


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

Upgrading the application
=========================

1. Get the latest version of source code::

        $ cd art17-consultation
        $ git pull origin master

2. Update the application stack, all services should be "Up" ::

        $ docker-compose up -d
        $ docker-compose ps


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


Factsheet generator
-------------------

Printouts work using `wkhtmltopdf 0.12.1`. Using another version may cause
problems in rendering pdfs.

If you don't have this version installed, add it to your virtualenv.

1. Go to http://sourceforge.net/projects/wkhtmltopdf/files/0.12.1/ and select the build
   corresponding with your system. Copy the direct link into your clipboard

2. Install it locally in your virtualenv

    * For RedHat-based systems in production::

         wget $PASTE_URL_COPIED_AT_STEP_1
         # $PACKAGE is the file downloaded with wget
         sudo rpm -i --prefix=/var/local/wkhtmltox-0.12.1 $PACKAGE.rpm
         # If the command fails because the file is already installed
         # copy `wkhtmltopdf` from the installation directory and skip
         # the next command
         cp /var/local/wkhtmltox-0.12.1/bin/wkhmtltopdf sandbox/bin/

    * For RedHat-based development systems::

         # If you don't work on projects that require other versions
         # Install this version globally
         wget $PASTE_URL_COPIED_AT_STEP_1
         sudo rpm -i $PACKAGE.rpm

    * For Debian based systems::

         wget $PASTE_URL_COPIED_AT_STEP_1
         dpkg-deb -x wkhtmltox-0.12.1_<your_distro>.deb sandbox
         cp sandbox/usr/local/bin/wkhtmltopdf sandbox/bin

Development instructions using Docker
-------------------------------------

Make sure you set DEBUG=True in app.env to reload the changes.

* Start stack, all services should be "Up" ::

        $ docker-compose up -d
        $ docker-compose ps

* Check application logs::

        $ docker-compose app

* When the image is modified you should update the stack::

        $ docker-compose up -d --build

* Delete the containers and the volumes with::

        $ docker-compose down -v

Debugging
=========

* Please make sure that `DEBUG=True` in `app.env` file.

* Update docker-compose.override.yml file `app` section with the following so that `docker-entrypoint.sh` is not executed::

        entrypoint: ["/usr/bin/tail", "-f", "/dev/null"]

* Attach to docker container and start the server in debug mode::

        $ docker exec -it art17consultation_app_1 bash
        # ./manage.py runserver -t 0.0.0.0 -p 5000

* See it in action: http://localhost:5000

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
