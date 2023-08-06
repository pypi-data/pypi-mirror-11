=====================
django-email-username
=====================

django-email-username allows the users of your Django-powered website to use their
email address to login, rather than using a separate username field.

|pypi| |build|

Using django-email-username
===========================

To enable ``django-email-username`` for your project you need to add ``emailusername`` to
``INSTALLED_APPS``::

    INSTALLED_APPS += ("emailusername", )

then add the following line to your ``settings.py``::

    AUTH_USER_MODEL = 'emailusername.User'

That's it!

Documentation
=============

Coming soon...

Installation
=============

You can install ``django-email-username`` either via the Python Package Index (PyPI)
or from source.

To install using ``pip``,::

    $ pip install django-email-username

To install using ``easy_install``,::

    $ easy_install django-email-username

You will then need to apply the migrations::

    $ python manage.py migrate emailusername

Downloading and installing from source
--------------------------------------

Download the latest version of ``django-email-username`` from
http://pypi.python.org/pypi/django-email-username/

You can install it by doing the following,::

    $ tar xvfz django-email-username-0.0.0.tar.gz
    $ cd django-email-username-0.0.0
    # python setup.py install # as root

Using the development version
------------------------------

You can clone the git repository by doing the following::

    $ git clone git://github.com/acordiner/django-email-username.git

Bug tracker
===========

If you have any suggestions, bug reports or annoyances please report them
at http://github.com/acordiner/django-email-username/issues/

License
=======

This software is licensed under the ``GPL v2 License``. See the ``LICENSE``
file in the top distribution directory for the full license text.


.. |pypi| image:: https://img.shields.io/pypi/v/django-email-username.svg?style=flat-square&label=latest%20version
    :target: https://pypi.python.org/pypi/django-email-username
    :alt: Latest version released on PyPi

.. |build| image:: https://img.shields.io/travis/acordiner/django-email-username/master.svg?style=flat-square&label=unix%20build
    :target: http://travis-ci.org/acordiner/django-email-username
    :alt: Build status of the master branch

.. |deps| image:: https://img.shields.io/requires/github/acordiner/django-email-username/master.svg?style=flat-square&label=dependencies
    :target: https://requires.io/github/acordiner/csvquerytool/requirements/?branch=master
    :alt: Status of dependencies