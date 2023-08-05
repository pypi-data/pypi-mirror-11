=============================
dj-paginator
=============================

.. image:: https://badge.fury.io/py/dj-paginator.png
    :target: https://badge.fury.io/py/dj-paginator

.. image:: https://travis-ci.org/pydanny/dj-paginator.png?branch=master
    :target: https://travis-ci.org/pydanny/dj-paginator

.. image:: https://coveralls.io/repos/pydanny/dj-paginator/badge.png?branch=master
    :target: https://coveralls.io/r/pydanny/dj-paginator?branch=master

A super-simple set of pagination tools for Django 1.8+

Documentation
------------------

The full documentation will soon be at https://dj-paginator.readthedocs.org.

Features
--------

* Super simple code base.
* Easy to create and switch themes.
* Really good documentation! (coming soon)
* Really good tests! (coming soon)
* Class-Based View mixin so you don't need to load template tags (coming soon)

Quickstart
----------

Install dj-paginator::

    pip install dj-paginator

In your installed apps::

    INSTALLED_APPS = [
        paginator
    ]

In your list view::

    class MyListView(ListView):
        model = MyModel
        paginate_by = 10

In your list view template::

    {% load paginator %}

    {% paginator %}

Done!

Switching to a new theme method 1
---------------------------------


::

    # Currently defaults to bootstrap.
    # I'll add foundation tomorrow.
    PAGINATOR_THEME = 'foundation'

Switching to a new theme method 2
---------------------------------

::

    {% load paginator %}

    {# Is the default #}
    {% bootstrap_paginator %}

    {# For when I add the foundation theme#}
    {% foundation_paginator %}




History
-------

0.1.0 (2015-07-26)
++++++++++++++++++

* First release on PyPI.
* Inception


