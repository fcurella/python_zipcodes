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
    >>> us_zipcodes.update() # downloads current version, compiles and caches it to disk
    
