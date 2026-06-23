*****
Roles
*****


Roles are sets of permissions that can be given to users. An user can have
zero, one or more roles.

The main roles used in the application are:

* Assessor
* National Expert
* Stakeholder
* Public User

An additional Administrator role exists, inheriting most of the Assessor
permissions, and giving access to additional features such as Site Configuration.


Particular Permissions
----------------------
For each user a `Show Assessment` checkbox is available, which, if unchecked,
will hide the latest assessments (both Automatic and Manual) from the view of that user.


Public User Permissions
-----------------------

The Public User can view assessments (but not add) and comment on them and on
the wiki pages.


Manual assessments
------------------

Public Users, Stakeholders and National Expert can only view assessments with "OK" decision.
Users that can add assessments, can also edit or mark as deleted (only for their own).
Only one assessment can be added per (country, biogeoregion, species/habitat) pair.

.. csv-table:: Add assessments
   :header: "User", "Add assessment", "Comment"
   :widths: 5, 5, 15

   "**Assessor**",✓,"Add for EU or member states which have reports"
   "**National Expert**",✓,"Add for EU or their own MS"
   "**Stakeholder**",✓,"Add for EU or member states which have reports"
   "**Public User**",,

.. csv-table:: Edit assessments
   :header: "User", "Edit own assessment", "Edit other user's assessment", "Comment"
   :widths: 5, 10, 15, 15

   "**Assessor**",✓,✓,"Can edit all fields."
   "**National Expert**",✓,,
   "**Stakeholder**",✓,,
   "**Public User**",,,

.. csv-table:: Delete assessments
   :header: "User", "Delete own assessment", "Delete other user's assessment", "Comment"
   :widths: 5, 10, 15, 15

   "**Assessor**",✓,,
   "**National Expert**",✓,,
   "**Stakeholder**",✓,,
   "**Public User**",,,

.. csv-table:: Set Decision
   :header: "User", "Set decisions on assessments"
   :widths: 10, 15

   "**Assessor**",✓
   "**National Expert**",
   "**Stakeholder**",
   "**Public User**",


Assessments comments
--------------------

Authenticated users can view and add comments on the manual assessments.
They can edit or delete their own comments. They can mark comments as read and see
the activity log (new unread comments, new conclusions).

.. csv-table:: Add/Edit/Delete comment
   :header: "User", "Add comment on own assessment", "Add comment on other user's assessment"
   :widths: 5, 10, 15

   "**Assessor**",✓,✓
   "**National Expert**",✓,
   "**Stakeholder**",✓,
   "**Public User**",,

Data sheet info and Data sheet info comments
============================================

Only Assessor users and Administrator users can add a new data sheet, edit the
existing one and restore a previous version.

Audit trails
===============================
Only Assessor users and Administrator users can add a new audit trail,
edit the existing one and restore a previous version.
