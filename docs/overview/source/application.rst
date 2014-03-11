Application
===========

The consultation tool is a Flask web application, running on a MySQL database
using SQLAlchemy as the ORM.

It runs in an isolated environment, using Virtualenv. The WSGI server used in
deployments is Waitress (in a combination with Apache2 mod_proxy).

Module structure
----------------

The main application module is `art17`. The main submodules are:

* `auth` - blueprint for authentication
* `app` - main application object
* `comments` - comments feature in summary views
* `models` - database abstraction
* `progress` - progress views
* `report` - report views
* `summary` - summary views and conclusion features
* `wiki` - datasheet info and audit trail

Other modules are: `assets`, `common`, `dataset`, `forms`, `layout`, `maps`, `mixins`, `utils`.

Source code summary
-------------------
