Changelog
=========

2.6 - (unreleased)
------------------

2.5 - (2017-05-09)
------------------
* Dockerise Article 17 consultation tool
  - create also the binds database
  - cleanup
  [chiridra refs #81735]

2.4 - (2017-05-05)
------------------
* Dockerise Article 17 consultation tool
  - use SCRIPT_NAME env variable to correctly set the "Recover password" url
  [chiridra refs #81735]

2.3 - (2017-04-24)
------------------
* removed hardcoded values for mysql server [nituacor refs #81735]

2.2 - (2017-04-21)
------------------
* Dockerise Article 17 consultation tool
  - processed two more env variables needed for production deploy
  [chiridra refs #81735]

2.1 - (2017-04-20)
------------------
* article17 staging
  - running gunicorn with -e SCRIPT_NAME=$SCRIPT_NAME to set
  the prefix (default is /)
  [chiridra refs #83820]

2.0 - (2017-03-30)
-----------------------
* Dockerise Article 17 consultation tool
  - discarded waitress and supervisor and used gunicorn
  - loaded settings from environment
  - major changes to Docker file: added docker-entrypoint script for
    running the app
  - added docker compose files version 2 for production and devel
    environments
  - added CHANGELOG.md file for tracking changes and keeping versions
  [chiridra refs #81735]

1.0 - (2013-01-01)
------------------
* Initial release
