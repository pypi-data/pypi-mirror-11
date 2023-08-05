Waterboy - Dynamic Application settings
=======================================

Store "live" application settings in a choice of key/value data stores.

This was originally a fork of `django-constance`_, but is now independent of
Django and is essentially the key/value abstraction part of the original library.

Backends currently supported: Redis and MongoDB.

Tested with Python 2.7 and Python 3.4.

The source is on `github`_.

Installation
------------

::

    $ pip install waterboy

Usage
-----

In your application, define the settings that you want to be editable::

    CONFIG = {
        '<KEY>': <DEFAULT>,
        ...
    }

For example::

    CONFIG = {
        'INT_VALUE': 1,
        'LONG_VALUE': 100000000,
        'BOOL_VALUE': True,
        'STRING_VALUE': 'Hello world',
        'UNICODE_VALUE': six.u('Rivière-Bonjour'),
        'DECIMAL_VALUE': Decimal('0.1'),
        'DATETIME_VALUE': datetime(2010, 8, 23, 11, 29, 24),
        'FLOAT_VALUE': 3.1415926536,
        'DATE_VALUE': date(2010, 12, 24),
        'TIME_VALUE': time(23, 59, 59),
    }

Then create a Config object based on these initial settings. For example, using Redis::

    >>> from waterboy import RedisConfig
    >>> cfg = RedisConfig(initial=CONFIG)

You then retrieve settings from the backend via attribute-style access::

    >>> cfg.INT_VALUE
    1

If the backend returns None then the default value is returned.

Similarly, setting an attribute on the Config object will transparently "upsert"
(update or insert) that value in the backend.

Attempts to get or set values on the Config object will fail with an AttributeError
if the key does not exist in the initial defaults dictionary::

    >>> cfg.ABCD = 'abcd'
    Traceback (most recent call last):
      ...
    AttributeError: 'RedisConfig' object has no attribute 'ABCD'

But this behaviour may be modified by passing **strict=False** to the Config constructor::

    >>> cfg = RedisConfig(initial=CONFIG, strict=False)

which will cause the existence check to be bypassed::

    >>> cfg.ABCD = 'abcd'

Development
-----------

Clone and run tests::

    $ git clone git@github.com:gmflanagan/waterboy.git
    $ cd waterboy
    $ make test

Tests are run via tox and pytest.

If redis and mongo are not running on the declared ports then the tests associated
with those backends will be skipped. See the makefile for the default ports.

To install redis and mongo locally, run buildout::

    $ make buildout

Then run redis in the foreground with::

    $ make redis

and mongodb with::

    $ make mongod

Now run all tests::

    $ make test

.. _django-constance: http://django-constance.readthedocs.org/
.. _waterboy: https://github.com/gmflanagan/waterboy
.. _github: https://github.com/gmflanagan/waterboy

