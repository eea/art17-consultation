Application
===========

The consultation tool is a Flask web application, running on a Postgres database
using SQLAlchemy as the ORM.

It runs in a Docker container (see the ``Dockerfile`` and ``docker-compose.yml``),
based on the ``python:3.12-slim`` image. The WSGI server used in deployments is
uWSGI (configured in ``uwsgi.ini``). When the container starts with ``MIGRATE=yes``,
the database migrations are applied with ``flask db upgrade``.

Errors are reported to Sentry when ``SENTRY_DSN`` is configured.

Module structure
----------------

The main application module is `art17`. The main submodules are:

* `admin` - Dataset Admin views (Flask-Admin)
* `auth` - blueprint for authentication
* `app` - main application object
* `comments` - comments feature in summary views
* `factsheet` - factsheets (PDF reports) for species/habitats
* `management` - command line commands (new reporting period, data import, ...)
* `models` - database abstraction
* `progress` - progress views
* `report` - report views
* `summary` - summary views and conclusion features
* `wiki` - datasheet info and audit trail

Other submodules are: `assets`, `common`, `dataset`, `forms`, `layout`, `maps`,
`mixins`, `pdf`, `queries`, `utils`.

Source code summary
-------------------

* `migrations/` - database migrations (Flask-Migrate / Alembic)
* `art17/` - main python application
* `art17/static/` - static files such as CSS or Javascript
* `art17/templates/` - HTML templates used in views
* `docs/` - documentation, user manual and overview
* `testsuite/` - unit testing
