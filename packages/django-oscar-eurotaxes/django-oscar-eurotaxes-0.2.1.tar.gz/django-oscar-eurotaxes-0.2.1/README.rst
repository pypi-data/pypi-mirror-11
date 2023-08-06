==============================
Taxes package for django-oscar
==============================

This package manage taxes on django-oscar_. The package is structured so that it can be used only with Oscar.

.. _django-oscar: https://github.com/tangentlabs/django-oscar

* `Full documentation`_

.. _`Full documentation`: http://django-oscar-paypal.readthedocs.org/en/latest/

License
-------

The package is released under the New BSD license.

Settings
--------

You must add `'eurotaxes.partner'` to `INSTALLED_APPS`
(replacing the equivalent Oscar app). This can be achieved using
Oscar's get_core_apps function - e.g.:

.. code-block:: python

    # settings.py
    ...
    INSTALLED_APPS = [
        'django.contrib.auth',
        ...
    ]
    from oscar import get_core_apps
    INSTALLED_APPS = INSTALLED_APPS + get_core_apps(
        ['eurotaxes.catalogue', 'eurotaxes.dashboard', 'eurotaxes.dashboard.catalogue', 'eurotaxes.partner']
    )

Commands
--------

You can use the command `oscar_populate_taxes` to add all the European Taxes.