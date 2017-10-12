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

SQLALCHEMY_BINDS = {
   'factsheet': '{schema}://{user}:{pwd}@{host}/{bindname}'.format(
        schema=getenv('DB_SCHEMA', default='sqlite'),
        user=getenv('DB_USER', default=''),
        pwd=getenv('DB_PASS', default=''),
        host=getenv('DB_HOST', default=''),
        bindname=getenv('BIND_NAME', default='')
    )
}

ASSETS_DEBUG = getenv('ASSETS_DEBUG', type=bool, default=False)
AUTH_DEBUG = getenv('AUTH_DEBUG', type=bool, default=False)

AUTH_LOG_FILE = getenv('AUTH_LOG_FILE', default='/var/local/art17/logs/flask-auth.log')
AUTH_ZOPE = getenv('AUTH_ZOPE', type=bool, default=True)
AUTH_ZOPE_WHOAMI_URL = getenv('AUTH_ZOPE_WHOAMI_URL', default='http://example.com/art17_api/whoami')
LAYOUT_ZOPE_URL = getenv('LAYOUT_ZOPE_URL', default='http://example.com/art17_api/layout')

AUTH_ZOPE_ACL_MANAGER_URL = getenv('AUTH_ZOPE_ACL_MANAGER_URL', default='http://example.com/acl_manager')
AUTH_ZOPE_ACL_MANAGER_KEY = getenv('AUTH_ZOPE_ACL_MANAGER_KEY', default='')

EEA_LDAP_SERVER = getenv('EEA_LDAP_SERVER', default='')

# Set this for correct links in emails.
if getenv('ART17_SERVER_NAME', default=None) is not None:
    ART17_SERVER_NAME = getenv('ART17_SERVER_NAME')
    SECURITY_EMAIL_SENDER = DEFAULT_MAIL_SENDER = 'noreply@' + ART17_SERVER_NAME
elif getenv('SERVER_NAME', default=None) is not None:
    SERVER_NAME = getenv('SERVER_NAME')
    SECURITY_EMAIL_SENDER = DEFAULT_MAIL_SENDER = 'noreply@' + SERVER_NAME

SECURITY_POST_REGISTER_VIEW = getenv('SECURITY_POST_REGISTER_VIEW', default='/article17/')

SENTRY_DSN = getenv('SENTRY_DSN', default='')

# Destination for PDF reports in the Factsheet module
PDF_DESTINATION = getenv('PDF_DESTINATION', default='./instance/pdf')
PDF_URL_PREFIX = getenv('PDF_URL_PREFIX', default='http://localhost:5000')

MAPS_STATIC = getenv('MAPS_STATIC', default='maps/')

DEMO_SERVER = getenv('DEMO_SERVER', type=bool, default=True)

SCRIPT_NAME = getenv('SCRIPT_NAME', default='/article17')

FACTSHEETS_REMOTE_URLS = {
    "2006": "https://forum.eionet.europa.eu/habitat-art17report/library/2001-2006-reporting/datasheets",
    "2012": "https://forum.eionet.europa.eu/habitat-art17report/library/2007-2012-reporting/factsheets"
}

FACTSHEETS_DOWNLOAD_URL = "download/en/1"
