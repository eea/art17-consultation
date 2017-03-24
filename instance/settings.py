# -*- coding: utf-8 -*-

from smart_getenv import getenv

# Turn this off on production
DEBUG = getenv('DEBUG', type=bool, default=False)

# This is mandatory. Please define a secret key - random sequence of characters
SECRET_KEY = getenv('SECRET_KEY', default='')

SQLALCHEMY_DATABASE_URI = '{schema}://{user}:{pwd}@{host}/{dbname}'.format(
  schema=getenv('DB_SCHEMA', default='sqlite'),
  user=getenv('DB_USER', default=''),
  pwd=getenv('DB_PASS', default=''),
  host=getenv('DB_HOST', default=''),
  dbname=getenv('DB_NAME', default=''))

#SQLALCHEMY_BINDS = {
#   'factsheet': 'mysql://user:password@localhost/art17old'
#}

# Fields below are optional. Update and uncomment the ones you need.

# ASSETS_DEBUG = False
# AUTH_DEBUG = False

# AUTH_LOG_FILE = '/var/local/art17/logs/flask-auth.log'
# AUTH_ZOPE = True
# AUTH_ZOPE_WHOAMI_URL = 'http://example.com/art17_api/whoami'
# LAYOUT_ZOPE_URL = 'http://example.com/art17_api/layout'

# AUTH_ZOPE_ACL_MANAGER_URL = 'http://example.com/acl_manager'
# AUTH_ZOPE_ACL_MANAGER_KEY = ''

# EEA_LDAP_SERVER = ''

# Set this for correct links in emails.
# SERVER_NAME = 'example.com'

# SECURITY_EMAIL_SENDER = DEFAULT_MAIL_SENDER = 'noreply@' + SERVER_NAME

# SECURITY_POST_REGISTER_VIEW = '/article17/'

# SENTRY_DSN = ''

# Destination for PDF reports in the Factsheet module
# PDF_DESTINATION = './instance/pdf'
# PDF_URL_PREFIX = 'http://localhost:5000'
