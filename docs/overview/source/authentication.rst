Authentication
==============

The authentication process is done externally, using Zope's builtin
authentication mechanism. This page describes the authentication process for a
registered user.

.. figure:: images/authentication.png
   :alt: Authentication Overview

   Authentication Overview

Backend
-------
The authorization is done using the Zope `/loggedin` view, which validates
the user credentials (externally to the Flask application), using either LDAP or
local stored accounts.

An authenticated session uses HTTP Basic Authentication. This means the browser
sends with every request a HTTP header with the authenticated user credentials.

Login Process
-------------

These are the steps explained:

#. The user accesses http://bd.eionet.europa.eu/article17/reports2012/ and
   clicks on the *Login* link in the top left part of the page.
#. A popup appears asking for credentials
#. The user enters the username and password for bd.eionet.europa.eu (either LDAP or local account)
#. The user is redirected to the home page of the consultation tool, and the *Login* link changes to *Logout (username)*.
