=======
Autotag
=======

Autotag is a simple Django app to conduct Web-based automatic tagging. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "autotag_app" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'autotag_app',
    )

2. Include the autotag_app URLconf in your project urls.py like this::

    url(r'^autotag_app/', include('autotag_app.urls')),

3. Run `python manage.py migrate` to create the autotag_app models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a autotag_app (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/autotag_app/ to participate in the autotag_app.


