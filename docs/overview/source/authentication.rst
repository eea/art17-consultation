Authentication
==============

The authentication process is done internally, either through LDAP or locally.
This page describes the authentication process for a registered user.

Backend
-------
The login is done through a form (``/auth/login``) and the authenticated session
is kept in a session cookie (Flask-Login). The credentials are checked first
against the EIONET LDAP server; if they are not valid there, they are checked
against the local accounts.

Login Process
-------------

These are the steps explained:

#. The user accesses https://nature-art17.eionet.europa.eu/article17/ and
   clicks on the *Login* link in the top left part of the page.
#. The login page asks for the username and password
#. The user enters the username and password for bd.eionet.europa.eu (either
   LDAP or local account)
#. The user is redirected to the home page of the consultation tool, and the
   *Login* link changes to *Logout (username)*.

An EIONET user logging in for the first time is registered automatically in the
local database, with the *Stakeholder* role. Users with the *Stakeholder* role
cannot log in after the consultation has ended.


Registration
-------------

By design and software specifications, the consultation is available for
anybody to both view and inspect the Biogeographical assessments. For other
purposes such as editing and actively participating into drawing conclusions,
one has to prior register for the consultation. As stated in the authentication
process there are two ways by which one can do so:

#. with an existing EIONET account (LDAP)
#. with a local user

For either one of the account types mentioned above, a new entry in the local
database is created.

The two types of accounts can be achieved by both self-registration and admin
workaround. This process is detailed in the **Art17 Consultation User Manual**,
the **Registration** section.
