Django Natural Key Cache
========================

|build-status| |coverage| |deps| |docs| |pypi|

Cache models via natural keys.

.. |build-status| image:: http://img.shields.io/travis/shadowfax-chc/django-natural-key-cache/master.svg?style=flat
    :alt: Build Status
    :scale: 100%
    :target: https://travis-ci.org/shadowfax-chc/django-natural-key-cache

.. |coverage| image:: http://img.shields.io/coveralls/shadowfax-chc/django-natural-key-cache.svg?style=flat
    :alt: Coverage Status
    :scale: 100%
    :target: https://coveralls.io/r/shadowfax-chc/django-natural-key-cache?branch=master

.. |deps| image:: http://img.shields.io/gemnasium/shadowfax-chc/django-natural-key-cache.svg?style=flat
    :alt: Dependency Status
    :scale: 100%
    :target: https://gemnasium.com/shadowfax-chc/django-natural-key-cache

.. |docs| image:: https://readthedocs.org/projects/django-natural-key-cache/badge/
    :alt: Documentation Status
    :scale: 100%
    :target: http://django-natural-key-cache.readthedocs.org/en/latest/

.. |pypi| image:: http://img.shields.io/pypi/v/django-natural-key-cache.svg?style=flat
    :alt: PyPi version
    :scale: 100%
    :target: https://pypi.python.org/pypi/django-natural-key-cache


Quick Start
-----------

Add manager to model.

.. code-block:: python

    from django.db import models
    from natural_key_cache.cache_manager import NaturalKeyCacheManager

    class MyModel(models.Model):
        # Define natural keys, this can be ommited if id/pk is the natural key
        natural_keys = (
            'nat_key',
        )
        cache = NaturalKeyCacheManager(natural_keys)
        nat_key = models.CharField(max_length=32, unique=True)

Then access the cached model via the new manager.

.. code-block:: python

    MyModel.cache.get(nat_key='unique_instance')
