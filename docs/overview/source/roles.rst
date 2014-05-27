.. _roles-label:

Roles
=====

Roles are sets of permissions that can be given to users. An user can have
zero, one or more roles.

The main roles used in the application are:

* ETC/BD Expert
* Stakeholder
* National Expert
* Public User

An additional Administrator role exists, inheriting most of the ETC/BD Expert
permissions, and giving access to additional features such as Site Configuration.

Common Permissions
------------------
All authenticated users can view and add comments on the manual assessments, and on the
the datasheet info. They can edit or delete their own comments. They can mark
comments as read and see the activity log (new unread comments, new
conclusions).

Users that can add assessments, can also edit or mark as deleted (only for their
own). Only one assessment can be added per (country, biogeoregion,
species/habitat) pair.

All authenticated users except for Public Users can edit the Wiki Trail and
Datasheet Info pages.

ETC/BD Expert Permissions
-------------------------

The ETC/BD Expert can add assessments at EU27 level. It can also edit the
reference values in other users' conclusions.

It can set a decision for all the assessments.

Stakeholder Permissions
-----------------------

The Stakeholder can add assessments for different member states.

National Expert Permissions
---------------------------

The National Expert can add assessments only for his/her member state.


Public User Permissions
-----------------------

The Public User can view assessments (but not add) and comment on them and on
the wiki pages.
