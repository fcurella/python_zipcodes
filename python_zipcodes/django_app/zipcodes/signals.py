from python_zipcodes.countries import country_list
from python_zipcodes.importers import ZipCodeManager
from python_zipcodes.storages import DjangoStorage

def save_zipcodes(sender, app, created_models, **kwargs):

    zc_manager = ZipCodeManager(storage=DjangoStorage)
    for c in country_list:
        zc_manager.add(c)
        if sender.ZipCode.objects.filter(country=c).count() == 0:
            zc_manager[c].update()
            #for zc, data in zc_manager.zipcodes(c).items():
            #    sender.ZipCode.objects.create(zipcode=zc, city=data['city'], state=data['state'], country=c)

