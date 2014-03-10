Database
========

This page describes the database structure. We're using the term *Dataset* to describe
a set of data for a given reporting period (such as 2001-2006).

.. figure:: images/database.png
   :alt: Database structure

   The Database

Structure
---------
The tables can be classified *by content* in:

#. initial content tables (ETC/BD member states data - \*_regions, Automatic Assesments - \*_automatic_assessments)
#. dictionary tables (Country codes, Method details, Trend details, ... \*_dic_\*)
#. user contributed content (Conclusions - \*_manual_assessments, Comments on conclusions - \*_comments, Datasheet info, Audit trail - \*wiki\*)
#. application specific (Registered Users, Configuration, Dataset information).

Each of the tables in the first three categories contain a column named *ext_dataset_id* linking
 to the dataset the record belongs to.

Backend
-------

We're using a single database on a MySQL server running on localhost.

