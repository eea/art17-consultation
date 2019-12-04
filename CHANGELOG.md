Changelog
=========

3.1.0 - (2019-12-04)
-------------------
* Fix security issues
  [dianaboiangiu]
  
3.0.9 - (2019-11-22)
--------------------
* Add maps urls for new period
  [dianaboiangiu]

3.0.8 - (2019-11-18)
--------------------
* Fix Greece original link
  [dianaboiangiu]

3.0.7 - (2019-11-15)
--------------------
* Set order for methods
* Display min, max, best values with 2 decimals
* Add newlines for MS value
  [dianaboiangiu]

3.0.6 - (2019-11-13)
--------------------
* Fix automatic species method
  [dianaboiangiu]

3.0.5 - (2019-11-13)
--------------------
* Add revision for datasheets
  [dianaboiangiu]

3.0.4 - (2019-11-11)
--------------------
* Add species lu new fields
  [dianaboiangiu]

3.0.3 - (2019-11-08)
--------------------
*  Fix Dockerfile wkhtmltopdf
  [dianaboiangiu]

3.0.2 - (2019-11-08)
--------------------
* Mody species text for period 2013
  [dianaboiangiu]

3.0.1 - (2019-11-07)
--------------------
* Mody text for period 2013
  [dianaboiangiu]

3.0.0 - (2019-11-07)
--------------------
* Release new period 2013-2018
  [dianaboiangiu]

2.11.5 - (2019-07-10)
--------------------
* Exposed Progress view now includes all groups
  [dianaboiangiu]

2.11.4 - (2019-07-09)
--------------------
* Use Eionet password reset link
  [dianaboiangiu]

2.11.3 - (2019-06-26)
-------------------
* Small fixes authentication
  [dianaboiangiu]

2.11.2 - (2019-06-26)
-------------------
* Set change password link
  [dianaboiangiu]

2.11.1 - (2019-06-21)
-------------------
* Remove eionet headers
* Move application authentication to Ldap server
  [dianaboiangiu]

2.11.0 - (2019-06-12)
-------------------
* Migrate header and footer to new Plone templates
  [dianaboiangiu]

2.10.9 - (2018-10-15)
-------------------
* Small fixes progress table view
  [dianaboiangiu]

2.10.8 - (2018-10-15)
-------------------
* Set new note for 2012bis period
* Add demo progress view
  [dianaboiangiu]

2.10.7 - (2018-09-12)
-------------------
* Add log message for static collecting in docker entrypoint
  [dianaboiangiu]

2.10.6 - (2018-09-12)
-------------------
* Simulate collect static for flask application
  [dianaboiangiu]

2.10.5 - (2018-09-11)
-------------------
* Set secure css link
  [dianaboiangiu]

2.10.4 - (2018-07-10)
-------------------
* Fix 2012bis manual assessment
  [dianaboiangiu]

2.10.3 - (2018-06-25)
-------------------
* Implement 2012bis feedback
  [dianaboiangiu]

2.10.2 - (2018-06-15)
-------------------
* Fix Dockerfile libmsqlclient package
  [dianaboiangiu]

2.10.1 - (2018-06-13)
-------------------
* Add cdr links to summary/report
  [dianaboiangiu]

2.10.0 - (2018-05-25)
-------------------
* Fixes for period 2012bis
  [dianaboiangiu]

2.9.9 - (2018-04-20)
-------------------
* Prepare 2012bis period
  [dianaboiangiu]

2.9.8 - (2018-03-20)
-------------------
* Fix travis settings file
  [dianaboiangiu]

2.9.7 - (2018-03-20)
-------------------
* Remove user permissions for staging tests
  [dianaboiangiu]

2.9.6 - (2018-03-20)
-------------------
* Add period dynamic filtering of countries on reports
* Add command for importing greece
  [dianaboiangiu]

2.9.5 - (2018-02-15)
-------------------
* Add README badges
* Fix summary for 2012bis period
  [dianaboiangiu]

2.9.4 - (2018-02-15)
-------------------
* Fix auto assessment button show
  [dianaboiangiu]

2.9.3 - (2018-02-14)
-------------------
* Prepare application for new period 2012bis
  [dianaboiangiu]

2.9.2 - (2018-01-30)
--------------------
* Fix docker error
  [nico4]

2.9.1 - (2018-01-30)
--------------------
* Switch to semantic versioning
* Follow redirects in Dockerfile
  [nico4]

2.9 - (2018-01-30)
------------------
* Fix docker install wkhtmltopdf
  [nico4]

2.8 - (2018-01-30)
------------------
* Fix factsheets remote urls
  [catalinjitea]

2.7 - (2017-06-09)
------------------
* Improve README for docker installation
  [iuliachiriac]

2.6 - (2017-05-10)
------------------
* Missing factsheets in dockerized article 17 si article 12
  [chiridra refs #84975]

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
