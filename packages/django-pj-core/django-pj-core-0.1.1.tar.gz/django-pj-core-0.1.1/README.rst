=============================
django-pj-core
=============================

.. image:: https://badge.fury.io/py/django-pj-core.png
    :target: https://badge.fury.io/py/django-pj-core

.. image:: https://travis-ci.org/jokimies/django-pj-core.png?branch=master
    :target: https://travis-ci.org/jokimies/django-pj-core

Misc utilities for Django

Documentation
-------------

The full documentation is at https://django-pj-core.readthedocs.org
(someday, not yet).

Quickstart
----------

Install django-pj-core::

    pip install django-pj-core

Then use it in a template::

    {% load pjcore_tags %}

    ... class="{{ value | colorize_percentage }}" ...

Will return string `red` (negative ``value`` or `green` (positive ``value``)


Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage
