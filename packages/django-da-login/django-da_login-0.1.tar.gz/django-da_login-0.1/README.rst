=====
Da Login
=====

Da Login is a simple Django app to register and login to system.
Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "da_login" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'da_login',
    )

2. Include the polls URLconf in your project urls.py like this::
   (r'', include('da_login.urls', namespace='da_login', app_name='da_login')),


3. Run `python manage.py migrate` to create the polls models.

5. Visit http://127.0.0.1:8000/register/ to register or http://127.0.0.1:8000/login/ to login.