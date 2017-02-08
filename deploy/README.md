# Docker orchestration for Art 17 Consultation Tool

## 1. Usage

Clone the repository

    $ git clone https://github.com/eea/art17-consultation

During the first time deployement, create and edit the following files:

    $ cd art17-consultation/deploy

    # edit environment variables values
    $ cp art17.env.example art17.env
    $ vim art17.env

    # setup SSH key for rsync service
    $ cp rsync.key.example rsync.key
    $ vim rsync.key

## 2. Production

The production deployment will be done through Rancher. Depending on the
Rancher environment's version, one of the following will be used:

1. [Rancher Compose](https://docs.rancher.com/rancher/v1.4/en/cattle/rancher-compose/)

2. [Rancher CLI](https://docs.rancher.com/rancher/v1.2/en/cli/)

_WIP_

## 3. Development

1. Install [Docker](https://www.docker.com/).

2. Install [Docker Compose](https://docs.docker.com/compose/).


### 3.1 Local build

To use a local build, run the following command:

    $ docker build -t art17:devel .

and in docker-compose.yml use for art17 service:

    image: art17:devel

Start services

    $ cd art17-consultation/deploy/art17-devel
    $ docker-compose up -d

    #show services and their status
    $ docker-compose ps

### 3.2. Art 17 service

There is a mapping between your local art17 folder and the folder inside the service.
Any code change will be automatically detected and the app restarted.

    # view logs
    $ docker-compose logs -f art17

Still, if a syntax error occurs the service will stop working and therefore must be
manually restarted:

    # restart service
    $ docker-compose restart art17

Another approach is to step in the container and manually start/stop the app.
To do that, in docker-compose.yml file change for art17 service the _command_ as below:

    command: /usr/bin/tail -f /dev/null

and after:

    # upgrade service
    $ docker-compose up -d art17

    # step into the art17 container
    $ docker exec -it art17devel_mysql_1 bash

and from inside the container:

    # manually start app
    $ python manage.py runserver -t 0.0.0.0 -p 5000

_Note: make sure you have set **DEBUG=True** in the art17.env file._

### 3.3. MySQL service

If you need to take a closer look at the MySQL database, you can do that like below:

    # step into the mysql container
    $ docker exec -it art17devel_mysql_1 bash

    # start mysql client
    $ mysql -u root -p

    # runn SQL commands
    mysql> use DB_NAME;
    mysql> show tables;

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

