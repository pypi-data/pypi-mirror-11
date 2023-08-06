=============================
django-statuspage
=============================

.. image:: https://badge.fury.io/py/django-statuspage.png
    :target: https://badge.fury.io/py/django-statuspage

.. image:: https://travis-ci.org/marguslaak/django-statuspage.png?branch=master
    :target: https://travis-ci.org/marguslaak/django-statuspage

Display status and information of the system. Can be used as a heartbeat
indicator for load balancer.

Quickstart
----------

Install django-statuspage::

    pip install django-statuspage

Then use it in a project::

    import djstatuspage

Features
--------

* Display information about installed system with a simple json response

Usage
-----

Add url in your project with

import djastatuspage

urlpatterns += patterns('',
    url(r'^', include(djstatuspage.urls.urlpatterns, namespace='statuspage')),
)

Settings
--------

*  STATUSPAGE_TASKS - define extra callables to add to output in key-value
manner. For example.

    STATUSPAGE_TASKS["version"] = lambda: "0.1.0"

Will return

    {"database": "ok", "version": "0.1.0"}

*  STATUSPAGE_TRY_DATABASE - Default True. Turn off database round trip.


Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage
