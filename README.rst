Python Zipcodes
======================================

A small little module for building zipcodes dictionaries and easily updating them.

Includes some precompiled zipcodes. Currently:

  * US

Usage
-----

    >>> from python_zipcodes.importers import ZipCodeManager
    >>> zc_manager = ZipCodeManager()
    >>> zipcodes = zc_manager().zipcodes('US') # country code is case-insensitive. First call will take some time. 
    >>> zipcodes['us'].has_key('66044')
    True
    >>> zipcodes['us']['66044']
    {'city:'Lawrence', 'state':KS'}
    >>> zipcodes.find('us','66044')
    {'city:'Lawrence', 'state':KS'}
    
Using with Django::

    1. Add `python_zipcodes.django_app.zipcodes` to `INSTALLED_APPS`
    2. Run `sync_db`

API w/ Django::

    >>> from python_zipcodes.django_app.zipcodes.models import ZipCode
    >>> from python_zipcodes.storages import DjangoStorage
    >>> zc_manager = ZipCodeManager(storage=DjangoStorage, model=ZipCode)
    >>> zipcodes = zc_manager().zipcodes('US') # country code is case-insensitive. First call will take some time. 
