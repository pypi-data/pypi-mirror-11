django-nopassword
=================

|Build status| |PyPi version| |Wheel Status| |Downloads| |Requirements
Status| |License|

This project was originally inspired by `Is it time for password-less
login? <http://notes.xoxco.com/post/27999787765/is-it-time-for-password-less-login>`__
by `Ben Brown <http://twitter.com/benbrown>`__

Installation
------------

Run this command to install django-nopassword

::

    pip install django-nopassword

Requirements
~~~~~~~~~~~~

Django >= 1.4 (1.5 custom user is supported)

Usage
-----

Add the app to installed apps

.. code:: python

    INSTALLED_APPS = (
        ...
        'nopassword',
        ...
    )

Set the authentication backend to *EmailBackend*

::

    AUTHENTICATION_BACKENDS = ( 'nopassword.backends.email.EmailBackend', )

Add urls to your *urls.py*

.. code:: python

    urlpatterns = patterns('',
        ...
        url(r'^accounts/', include('nopassword.urls')),
        ...
    )

Settings
~~~~~~~~

Information about the available settings can be found in the
`docs <http://django-nopassword.readthedocs.org/en/latest/#settings>`__

Tests
-----

Run with ``python setup.py test``. To run with sqlite add
``USE_SQLITE = True`` in tests/local.py

--------------

MIT © Rolf Erik Lekang

.. |Build status| image:: https://ci.frigg.io/badges/relekang/django-nopassword/
   :target: https://ci.frigg.io/relekang/django-nopassword/
.. |PyPi version| image:: https://pypip.in/v/django-nopassword/badge.png
   :target: https://crate.io/packages/django-nopassword/
.. |Wheel Status| image:: https://pypip.in/wheel/django-nopassword/badge.svg
   :target: https://pypi.python.org/pypi/django-nopassword/
.. |Downloads| image:: https://pypip.in/download/django-nopassword/badge.svg
   :target: https://pypi.python.org/pypi/django-nopassword/
.. |Requirements Status| image:: https://requires.io/github/relekang/django-nopassword/requirements.svg?branch=master
   :target: https://requires.io/github/relekang/django-nopassword/requirements/?branch=master
.. |License| image:: https://pypip.in/license/django-nopassword/badge.svg
   :target: https://pypi.python.org/pypi/django-nopassword/


