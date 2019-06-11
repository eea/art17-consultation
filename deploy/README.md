# Docker orchestration for Art 17 Consultation Tool

Clone the repository

    $ git clone https://github.com/eea/art17-consultation

During the first time deployement, create and edit the following file:

    $ cd art17-consultation/deploy

    # setup SSH key for rsync service
    $ cp rsync.key.example rsync.key
    $ vim rsync.key

[Base docker image](https://hub.docker.com/r/eeacms/art17-consultation/)

## 1. Production

The production deployment will be done through Rancher. Depending on the
Rancher environment's version, one of the following will be used:

1. [Rancher Compose](https://docs.rancher.com/rancher/v1.4/en/cattle/rancher-compose/)

2. [Rancher CLI](https://docs.rancher.com/rancher/v1.2/en/cli/)

During the first time deployement, create and edit the following files:

    $ cd art17-consultation/deploy

    # edit environment variables values
    $ cp art17.env.example art17.env
    $ vim art17.env

### 1.1. Start stack

    $ cd art17-consultation/deploy/art17/
    $ docker-compose up -d

### 1.2. Configure _apache_ service

Copy conf file and restart container

    $ scp -P 2222 ../conf/apache.conf root@rsync-server-host:/usr/local/apache2/conf/extra/vh-my-app.conf
    $ docker-compose restart apache

### 1.3. Configure _art17-static_ service

Copy conf file and restart container

    $ scp -P 2222 ../conf/static.conf root@rsync-server-host:/etc/nginx/conf.d/default.conf
    $ docker-compose restart art17-static

### 1.4 Copy _mysql_ data (SQL dump)

    $ scp -P 2222 art17.sql root@rsync-server-host:/var/lib/mysql/art17.sql

Execute shell to _mysql_ container and import the sql file.

    $ mysql -u root -p
    $ mysql> use art17;
    $ mysql> source /var/lib/mysql/art17.sql;

### 1.5. Debugging

Please refer to points 3.5. - 3.7. below.

## 2. Staging

The production deployment will be done also through Rancher.

During the first time deployement, create and edit the following files:

    $ cd art17-consultation/deploy

    # edit environment variables values
    $ cp art17.env.example art17.staging.env
    $ vim art17.staging.env

### 2.1. Start stack

    $ cd art17-consultation/deploy/art17-staging/
    $ docker-compose up -d

### 2.2. Configure _apache_ service

Please refer to point 1.2.

### 2.3. Configure _art17-static_ service

Please refer to point 1.3.

### 2.4 Copy _mysql_ data (SQL dump)

    $ scp -P 2222 art17_staging.sql root@rsync-server-host:/var/lib/mysql/art17_staging.sql

Execute shell to _mysql_ container and import the sql file.

    $ mysql -u root -p
    $ mysql> use art17_staging;
    $ mysql> source /var/lib/mysql/art17_staging.sql;

### 2.5. Debugging

Please refer to points 3.5. - 3.7. below.

## 3. Development

1. Install [Docker](https://www.docker.com/).

2. Install [Docker Compose](https://docs.docker.com/compose/).

During the first time deployement, create and edit the following files:

    $ cd art17-consultation/deploy

    # edit environment variables values
    $ cp art17.env.example art17.devel.env
    $ vim art17.devel.env

A minimal configuration file could be:

    #mysql env
    MYSQL_ROOT_PASSWORD=art17

    #art17 env
    DEBUG=True
    SECRET_KEY=secret

    DB_SCHEMA=mysql
    DB_USER=art17
    DB_PASS=art17
    DB_HOST=mysql
    DB_NAME=art17
    BIND_NAME=art17rp2_eu

    AUTH_PLONE=False


### 3.1. Local `docker-compose.yml` file

    $ cd art17-consultation/deploy/art17-devel/
    $ cp docker-compose.yml.example docker-compose.yml

### 3.2. Local build

To use a local build, run the following command:

    $ cd art17-consultation/
    $ docker build -t art17:devel .

and in docker-compose.yml use for art17 service:

    image: art17:devel

### 3.3. Developing and debugging

In order for your container to see the latest updates made to the code, you
have to use a volume. Uncomment the following lines in `docker-compose.yml`:

    #volumes:
    #- ../../art17:/var/local/art17/art17/

To debug the application, first override the command used by the image.
Uncomment this line:

    #command: /usr/bin/tail -f /dev/null

After starting the stack (see 2.4 below), start the development server from
inside the container. The execution will stop and wait for your commands every
time it encounters a breakpoint in your code.

    $ docker exec -it art17-app bash
    $ ./manage.py runserver -t 0.0.0.0 -p 5000


### 3.4. Start stack

    $ cd art17-viewer/deploy/art17-devel/
    $ docker-compose up -d

### 3.5. View, check status and logs

To use the application, open a browser/tab and got to http://localhost:5000/.

Other command line useful commands:

    $ # list services and their status
    $ docker-compose ps

    $ # view log
    $ docker-compose logs -f

If, for some reason, you want to completely delete the stack and its volumes:

    $ docker-compose stop
    $ docker-compose rm
    $ docker volume rm art17_mysqldata

### 3.6. _art17-app_ service

There is a mapping between your local art17 folder and the folder inside the service.
Any code change will be automatically detected and the app restarted.

    # view logs
    $ docker-compose logs -f art17-app

Still, if a syntax error occurs the service will stop working and therefore must be
manually restarted:

    # restart service
    $ docker-compose restart art17-app

Another approach is to step in the container and manually start/stop the app.
To do that, in docker-compose.yml file change for _art17-app_ service the _command_ as below:

    command: /usr/bin/tail -f /dev/null

and after:

    # upgrade service
    $ docker-compose up -d art17-app

    # step into the art17-app container
    $ docker exec -it art17-app bash

and from inside the container:

    # manually start the app
    $ python manage.py runserver -t 0.0.0.0 -p 5000

_Note: make sure you have set **DEBUG=True** in the art17.devel.env file._

### 3.7. _mysql_ service

If you need to take a closer look at the MySQL database, you can do that like below:

    # step into the mysql container
    $ docker exec -it art17-mysql bash

    # start mysql client
    $ mysql -u root -p

    # runn SQL commands
    mysql> use DB_NAME;
    mysql> show tables;

To import old data, first copy the sql dumps to your mysql container:

    $ docker cp art17.sql art17-mysql:/var/lib/mysql/

    # step into the mysql container
    $ docker exec -it art17-mysql bash

    # start mysql interpreter
    $ mysql -u art17 -p

    # import data
    mysql> use art17;
    mysql> source /var/lib/mysql/art17.sql

Do the same set of operations for `art17rp2_eu` database.

### 3.8. Factsheets

Create factsheets:

    $ docker exec -it art17-app bash
    $ ./manage.py factsheet genall [period_id]

_Note: make sure you also have the development server running._

## Copyright and license

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The Original Code is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

## Funding

[European Environment Agency (EU)](http://eea.europa.eu)

