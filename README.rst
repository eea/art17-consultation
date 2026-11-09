Art 17 Consultation Tool
=========================
https://nature-art17.eionet.europa.eu/article17/reports2012

|docker|

.. |docker| image:: https://img.shields.io/docker/build/eeacms/art17-consultation
   :target: https://hub.docker.com/r/eeacms/art17-consultation/

.. contents ::

Prerequisites
=============

1. Install `Docker`_ (with the `Docker Compose`_ plugin)

.. _`Docker`: https://docs.docker.com/engine/install/
.. _`Docker Compose`: https://docs.docker.com/compose/install/

The application image is built from the ``Dockerfile`` (Python 3.12) and runs
with a PostgreSQL 13 database container.

Installing the application
==========================

1. Get the source code::

        $ git clone https://github.com/eea/art17-consultation.git
        $ cd art17-consultation

2. Customize env files::

        $ cp docker/app.env.example docker/app.env
        $ cp docker/db.env.example docker/db.env

   Set at least ``SECRET_KEY``, the ``DB_*`` values and ``POSTGRES_PASSWORD``.
   Use ``DEBUG=False`` and ``AUTH_DEBUG=False`` outside development.

3. Create ``docker/init.sql``, used by the database container to create the
   application databases on its first start (it is not part of the repository)::

        CREATE USER art17prod WITH PASSWORD '<DB_PASS>';
        CREATE DATABASE art17prod;
        GRANT ALL PRIVILEGES ON DATABASE art17prod TO art17prod;
        CREATE DATABASE art17_eu;
        GRANT ALL PRIVILEGES ON DATABASE art17_eu TO art17prod;

   The user, password and database names must match ``DB_USER``, ``DB_PASS``,
   ``DB_NAME`` and ``BIND_NAME`` from ``docker/app.env``.

4. Customize docker orchestration::

        $ cp docker-compose.override.yml.example docker-compose.override.yml

5. Start stack, all services should be "Up" ::

        $ docker compose up -d --build
        $ docker compose ps

   The database migrations are applied when the app container starts with
   ``MIGRATE=yes``; to run them manually::

        $ docker compose exec app python -m flask db upgrade

6. Create your user and assign admin role to it::

        # for local user
        $ docker compose exec app python -m flask users create id:<user_id> email:<user_email> --password '<password>' --active
        # for Eionet user: log in once with the Eionet account (the user is
        # registered automatically), then make it admin

        # make it admin
        $ docker compose exec app python -m flask roles add <user_email> admin

Configuration
-------------
The application is configured through the environment variables from
``docker/app.env`` (read by ``instance/settings.py``); ``docker/app.env.example``
lists all of them.

Configuring the LDAP SERVER
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The authentication is provided by a LDAP SERVER (with a fallback to local
accounts). Add the following configuration variables to ``docker/app.env``,
using the correct values for the LDAP server::

    EEA_LDAP_PROTOCOL=ldaps
    EEA_LDAP_SERVER=ldap.example.com
    EEA_LDAP_PORT=636

Upgrading the application
=========================

1. Get the latest version of source code::

        $ cd art17-consultation
        $ git pull origin master

2. Rebuild and update the application stack, all services should be "Up" ::

        $ docker compose up -d --build
        $ docker compose ps

3. Apply the database migrations (if ``MIGRATE`` is not set to ``yes``)::

        $ docker compose exec app python -m flask db upgrade


Development hints
=================

Requirements
------------

Use ``requirements-dev.txt`` instead of ``requirements-dep.txt``::

    pip install -r requirements-dev.txt


Running unit tests
------------------

The tests use an in-memory SQLite database. Inside the app container (with the
development requirements installed) run::

    $ docker compose exec app python -m pytest testsuite

For a bit of speedup you can install ``pytest-xdist`` and run tests in
parallel, ``python -m pytest testsuite -n 4``.


Factsheet generator
-------------------

The factsheets for the periods 2001-2006 and 2007-2012 are served from
``FACTSHEETS_REMOTE_URL``.

Generating the PDF factsheets locally (``flask factsheet species`` /
``flask factsheet habitat``) requires `wkhtmltopdf 0.12.1`, which is not
installed in the Docker image. Using another version may cause problems in
rendering pdfs.

New reporting period
--------------------

The commands used to create a new reporting period and import its data
(``generate_new_period`` and ``import_new_data``) are described in the
*Art17 Consultation Overview* documentation, the **Database** section. All the
available commands are listed by ``python -m flask --help``.

Development instructions using Docker
-------------------------------------

Make sure you set ``DEBUG=True`` in ``docker/app.env`` to reload the changes.

* Start stack, all services should be "Up" ::

        $ docker compose up -d
        $ docker compose ps

* Check application logs::

        $ docker compose logs -f app

* When the image is modified you should update the stack::

        $ docker compose up -d --build

* Delete the containers and the volumes with::

        $ docker compose down -v

Debugging
=========

* Please make sure that ``DEBUG=True`` in ``docker/app.env`` file.

* The ``app`` section of ``docker-compose.override.yml.example`` already contains
  the following, so that ``docker-entrypoint.sh`` is not executed::

        entrypoint: ["/usr/bin/tail", "-f", "/dev/null"]

* Attach to docker container and start the server in debug mode::

        $ docker compose exec app bash
        # python -m flask run --debug -h 0.0.0.0 -p 5000

* See it in action: http://localhost:5000

Documentation
=============

Documentation can be found under ``docs``:

* Art17 Consultation User Manual::

        cd docs/user/
        make html

* Art17 Consultation Overview::

        cd docs/overview/
        make html

The User Manual configuration also loads the ``docxsphinx`` extension, so it must be
installed to build it. You can generate a docx file using::

        pip install docxsphinx
        cd docs/user
        sphinx-build -b docx source build

``docxsphinx`` requires an old ``docutils`` version (incompatible with ``rst2pdf``
from ``requirements.txt``), so install it in a separate virtualenv.


Contacts
========

The project owner is Søren Roug (soren.roug at eea.europa.eu)

Other people involved in this project are:

* Diana Boiangiu (diana.boiangiu at eaudeweb.ro)

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
Any recent Linux version with Docker and Docker Compose.
The PostgreSQL 13 database runs in the ``db`` container.


Copyright and license
=====================

This project is free software; you can redistribute it and/or modify it under
the terms of the EUPL v1.1.

More details under `LICENSE.txt`_.

.. _`LICENSE.txt`: https://github.com/eea/art17-consultation/blob/master/LICENSE.txt
