Python Zipcodes
======================================

A small little module for building zipcodes dictionaries and easily updating them.

Includes some precompiled zipcodes. Currently:

  * US

Usage
-----

    >>> from python_zipcodes.importers import ZipCodeManager
    >>> zc_manager = ZipCodeManager()
    >>> us_zipcodes = zc_manager().get('US') # country code is case-insensitive. First call will take some time. 
    >>> us_zipcodes.has_key('66044')
    True
    >>> us_zipcodes['66044']
    {'city:'Lawrence', 'state':KS'}
    
With Django:
    >>> from python_zipcodes.django_app.zipcodes.models import ZipCode
    >>> from python_zipcodes.storages import DjangoStorage
    >>> zc_manager = ZipCodeManager(storage=DjangoStorage, model=ZipCode)
    >>> us_zipcodes = zc_manager().get('US') # country code is case-insensitive. First call will take some time. 
    >>> us_zipcodes.has_key('66044')
    True
    >>> us_zipcodes['66044']
    {'city:'Lawrence', 'state':KS'}
