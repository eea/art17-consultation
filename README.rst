Art 17 Consultation
===================

1. Clone the repository::

    git clone git@github.com:eea/art17-consultation.git -o origin
    cd art17-consultation

2. Create & activate a virtual environment::

    virtualenv sandbox
    echo '*' > sandbox/.gitignore
    source sandbox/bin/activate

3. Install prerequisites if missing::

    python2.7 or higher
    apt-get install python-setuptools python-dev libmysqlclient-dev

4. Install dependencies::

    pip install -r requirements-dev.txt

5. Create a configuration file::

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

9. Run a test server::

    ./manage.py runserver



Data import
===========

Initially the application's database is empty. We need to import data
from a dump (the old 2006 app's database or the new reporting data).
First we need to load this dump into a separate MySQL databse::

    mysql -e 'create database art17_2006 CHARACTER SET utf8 COLLATE utf8_general_ci;'
    mysql art17_2006 < art17_2006.sql

Then we can import this data into our app's database. Make sure to
specify the right schema version, in this case '2006'::

    ./manage.py dataset import -d import-from-2006 -i 'mysql://user:pass@localhost/art17_2006' -s 2006


Configuring the Zope API
========================

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


Configure deploy
================

- copy fabfile/env.ini.example to fabfile/env.ini
- configure staging and production settings
- run fab staging deploy or fab production deploy
