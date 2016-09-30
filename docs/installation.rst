============
Installation
============

Download
========

Pip
---

Installation with pip is recommended in order to get the latest stable version::

    pip install django-helpcenter

From Source
-----------

You can also install the latest version of the code by pulling it directly from GitHub::

    pip install git+https://github.com/cdriehuys/django_helpcenter#egg=helpcenter

Django Configuration
====================

After downloading the app, add it to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        # default django apps here

        'helpcenter',

        # If you want to use the browseable api, add djangorestframework so
        # the static files are useable.
        'rest_framework',
    ]

Then add the appropriate urls to your project::

    urlpatterns = [
        # ...

        url(r'^help/', include('helpcenter.urls')),

        # ...
    ]

Post Installation
=================

After registering the app with Django, make sure to run the necessary migrations::

    python manage.py migrate
