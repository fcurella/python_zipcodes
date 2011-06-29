Python Zipcodes
======================================

A small little module for building zipcodes dictionaries and easily updating them.

Includes some precompiled zipcodes. Currently:

  * US

Usage
-----

    >>> from python_zipcodes.importers import ZipCodeManager
    >>> zc_manager = ZipCodeManager()
    >>> zc_manager.add('us') # country code is case-insensitive.
    >>> zipcodes = zc_manager['us'].zipcodes()
    >>> zipcodes['us'].has_key('66044')
    True
    >>> zipcodes['us']['66044']
    {'city:'Lawrence', 'state':KS'}
    >>> zipcodes.find('us','66044')
    {'city:'Lawrence', 'state':KS'}
    
Using with Django::

    1. Add `python_zipcodes.django_app.zipcodes` to `INSTALLED_APPS`
    2. Run `sync_db`

The App will expose a new model, `ZipCode`, composed of the following fields: `zipcode`, `country`,  `city`, `state`.

The database will be populated at the first `syncdb`, so it will take some time.

API w/ Django::

    >>> from python_zipcodes.storages import DjangoStorage
    >>> zc_manager = ZipCodeManager(storage=DjangoStorage)
    >>> zc_manager.add('us') # country code is case-insensitive.
    >>> zc_manager['us'].zipcodes()
    >>> zc_manager['us'].update() # downloads and saves to db. Takes some time.

or you could just use the plain DummyStorage::

    >>> zc_manager = ZipCodeManager()
    >>> zc_manager.add('us')
    >>> ZipCode.objects.get(state=zc_manager['us']['66044']['state'], country='us')