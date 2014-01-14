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
    mysql> create database art17;
    ./manage.py db upgrade

7. Import sql data dump in your art17 database::
    Due to rights policies we cannot make the data public.

8. Run a test server::

    ./manage.py runserver
