Python Zipcodes
======================================

A small little module for building zipcodes tables and updating them

Usage
-----

    >>> from python_zipcodes.importers import ZipCodes
    >>> us_zipcodes = ZipCodes('us')
    >>> us_zipcodes.has_key('66044')
    True
    >>> us_zipcodes['66044']
    ['Lawrence', 'KS']
    
