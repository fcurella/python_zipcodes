from python_zipcodes import ZipCodeManager
from nose.tools import assert_equal, assert_not_equal, assert_raises, assert_true

def test_basics():
    manager = ZipCodeManager()
    zipcodes = manager.zipcodes('US')
    zipcode = '66044'
    assert_true(zipcodes['us'].has_key(zipcode))
    assert_equal(zipcodes['us'][zipcode], {'city':'Lawrence', 'state':'KS'})
