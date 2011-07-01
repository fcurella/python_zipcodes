from python_zipcodes.countries import country_list
from python_zipcodes.importers import ZipCodeManager
import sys

def save_zipcodes(sender, app, created_models, **kwargs):

    zc_manager = ZipCodeManager()
    for c in country_list:
        zc_manager.add(c)
        if sender.ZipCode.objects.filter(country=c).count() == 0:
            if sys.argv[1] == 'test':
                zipcodes = [('10000', {'city': 'Test City', 'state': 'Test State'})]
            else:
                zipcodes = zc_manager[c].zipcodes().items()
            for zc, data in zipcodes:
                sender.ZipCode.objects.create(zipcode=zc, city=data['city'], state=data['state'], country=c)

