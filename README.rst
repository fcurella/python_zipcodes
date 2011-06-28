Python Zipcodes
======================================

A small little module for building zipcodes dictionaries and easily updating them.

Includes some precompiled zipcodes. Currently:

  * US

Usage
-----

    >>> from python_zipcodes.importers import ZipCodes
    >>> us_zipcodes = ZipCodes().get('US') # country code is case-insensitive 
    >>> us_zipcodes.has_key('66044')
    True
    >>> us_zipcodes['66044']
    ['Lawrence', 'KS']
    >>> us_zipcodes.update() # downloads current version, compiles and caches it to disk
    
