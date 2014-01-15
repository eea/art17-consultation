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
    apt-get install python-setuptools python-dev

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

8. Run a test server::

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
