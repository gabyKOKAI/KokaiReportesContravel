=====
ReportesVC
=====

Reportes Contravel para comisiones y ventas

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "ReportesVC" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'ReportesVC',
    ]

2. Include the ReportesVC URLconf in your project urls.py like this::

    url(r'^ReportesVC/', include('ReportesVC.urls')),

3. Run `python manage.py migrate` to create the ReportesVC models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create users and others (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ReportesVC/ to run reports in the ReportesVC.