*****
Roles
*****


Roles are sets of permissions that can be given to users. An user can have
zero, one or more roles.

The main roles used in the application are:

* Assessor
* Stakeholder
* Commission
* Public User (an authenticated user without any of the roles above)

An additional Administrator role exists, inheriting most of the Assessor
permissions, and giving access to additional features such as Site Configuration.

Most permissions also depend on the consultation period (see :doc:`Consultation <consultation>`)
and on the reporting period: nothing can be added, edited or commented on a
reporting period that is marked as read-only.


Particular Permissions
----------------------
For each user a `Show Assessment` checkbox is available, which, if unchecked,
will hide the latest assessments (both Automatic and Manual) from the view of that user.


Public User Permissions
-----------------------

The Public User can view assessments (but not add) and comment on them and on
the wiki pages.


Commission Permissions
----------------------

Commission users can view assessments, but cannot add assessments or comment on
assessments or on the data sheet info. When their name is hidden from other users,
they are shown as *Commission / EEA*.


Manual assessments
------------------

On the summary pages, all users can see the manual assessments, but only Assessor
and Administrator users can see the decision set for them. On the
*Summary of assessments by group* (progress) pages, only the assessments with an "OK"
decision are shown, to everyone except Administrators.

Only one assessment can be added per user for each (period, species/habitat, biogeoregion).

.. DocxTableStyle Table Grid

.. csv-table:: Add assessments
   :header: "User", "Add assessment", "Comment"
   :widths: 5, 5, 15

   "**Administrator**",✓,"Add for EU or member states which have reports"
   "**Assessor**",,
   "**Stakeholder**",✓,"Only during the consultation. Add for EU or member states which have reports"
   "**Commission**",,
   "**Public User**",,

.. DocxTableStyle Table Grid

.. csv-table:: Edit assessments
   :header: "User", "Edit own assessment", "Edit other user's assessment", "Comment"
   :widths: 5, 10, 15, 15

   "**Administrator**",✓,✓,"Can edit all fields."
   "**Assessor**",✓,✓,"Can edit all fields. Not possible during the consultation."
   "**Stakeholder**",✓,,"Only during the consultation."
   "**Commission**",,,
   "**Public User**",,,

.. DocxTableStyle Table Grid

.. csv-table:: Delete assessments
   :header: "User", "Delete own assessment", "Delete other user's assessment", "Comment"
   :widths: 5, 10, 15, 15

   "**Administrator**",✓,,
   "**Assessor**",✓,,"Not possible during the consultation."
   "**Stakeholder**",✓,,"Only during the consultation."
   "**Commission**",,,
   "**Public User**",,,

.. DocxTableStyle Table Grid

.. csv-table:: Set Decision
   :header: "User", "Set decisions on assessments"
   :widths: 10, 15

   "**Administrator**",✓
   "**Assessor**",✓
   "**Stakeholder**",
   "**Commission**",
   "**Public User**",


Assessments comments
--------------------

Authenticated users can view and add comments on the manual assessments.
Each user can add only one comment per assessment, and comments cannot be added to
deleted assessments. Users can edit or delete their own comments. They can mark comments
as read and see the activity log (new unread comments, new conclusions).

.. DocxTableStyle Table Grid

.. csv-table:: Add comment
   :header: "User", "Add comment on own assessment", "Add comment on other user's assessment", "Comment"
   :widths: 5, 10, 15, 15

   "**Administrator**",✓,✓,
   "**Assessor**",✓,✓,"Not possible during the consultation."
   "**Stakeholder**",✓,✓,"Only during the consultation, and only on assessments added by Stakeholders."
   "**Commission**",,,
   "**Public User**",,✓,

Data sheet info and Data sheet info comments
============================================

Only Assessor users and Administrator users can add a new data sheet, edit the
existing one and restore a previous version.

All authenticated users except Commission users can add one comment per data sheet
info, with the same consultation period restrictions as for assessment comments
(Stakeholders only during the consultation, Assessors not during the consultation).

Audit trails
===============================
Only Assessor users and Administrator users can add a new audit trail,
edit the existing one and restore a previous version.
