==================
Django View Export
==================

Generate CSV reports by simply creating SQL views.

Authenticated staff members can then directly download these reports as CSV.
It's a nice agile way to deal with the changing requirements for reports.


Quick start
-----------

1. Include the gifts URLconf in your project ``urls.py`` like this:

   .. code-block:: python

        url(r'^reports/', include('view_export.urls')),


2. Create an SQL view in your database:

   .. code-block:: sql

        => CREATE VIEW v_staff AS (
        ->      SELECT first_name, last_name FROM auth_user
        ->      WHERE is_staff = TRUE);

   You'll probably want to record this SQL in a file such as ``reports.sql`` or
   even better, add it to a Django migration.

3. Start the development server and visit ``http://127.0.0.1:8000/reports/staff/``
   or ``http://127.0.0.1:8000/reports/v_staff/`` to download the SQL view named
   ``v_staff`` as a CSV file.

No settings are required by default and there's no need to add the package to
Django's ``INSTALLED_APPS``.


Release History
---------------

0.5.4 (2015-08-09)
++++++++++++++++++

**Bugfixes**

 - Fix SQL injection vulnerability relating to "view" argument.


0.5.3 (2015-08-05)
++++++++++++++++++

**Improvements** 

 - Update documentation.
 - Rename PyPI package to ``django-view-export``.


