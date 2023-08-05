Sabot: Controlled failure for Django
====================================

|Logo|


Description
-----------
Provoke predictable errors in your Django projects. Raise OperationalErrors to
see how well your project handle database connection errors. Ideal for failure
tolerance testing.


License
-------

This project is open sourced under the `MIT License`_.


Installation
------------

.. code-block:: bash

    $ pip install django-sabot

* Add ``'sabot'``, to your project's ``INSTALLED_APPS`` list.
* Add some sabot patches in your settings.py file.


Usage
-----

In you settings.py file::

    from django.db import OperationalError

    from sabot.import *

    SABOT_PATCHES = (
        ConnectPatcher(error_generator=RandomErrorProducer, kwargs={'low': 1, 'high': 3}),
        CursorPatcher(error_producer=RandomErrorProducer, kwargs={'exception': OperationalError, 'low': 1, 'high': 10}),
        CursorPatcher(error_producer=CountErrorProducer, kwargs={'exception': OperationalError, 'number': 100, 'reset': True}),
        CursorPatcher(error_producer=TimeDeltaErrorProducer, kwargs={'exception': OperationalError, 'timedelta': {'seconds': 30}, 'reset': True}),
    )

A django-sabot patch is composed of a monkey patcher class and an error producer
class.

For example::

    CursorPatcher(error_producer=TimeDeltaErrorProducer, kwargs={'exception': OperationalError, 'timedelta': {'seconds': 30}, 'reset': True}),

will produce an OperationalError when a database cursor is requested, every 30
seconds.


Contribute
----------

- Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
- Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
- Write a test which shows that the bug was fixed or that the feature works as expected.
- Make sure to add yourself to the `AUTHORS file`_.
- Send a pull request

.. _`MIT License`: https://github.com/rosarior/django-sabot/blob/master/LICENSE
.. _`the repository`: http://github.com/rosarior/django-sabot
.. _`AUTHORS file`: https://github.com/rosarior/django-sabot/blob/master/AUTHORS.rst
.. |Logo| image:: https://github.com/rosarior/django-sabot/raw/master/docs/_static/logo.png
