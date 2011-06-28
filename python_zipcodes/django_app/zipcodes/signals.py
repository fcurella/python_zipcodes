from django.db.models.signals import post_syncdb
from python_zipcodes.countries import country_list
from python_zipcodes.django_app import zipcodes
from python_zipcodes.importers import ZipCodeManager

def save_zipcodes(sender, app, created_models, **kwargs):

    zc_manager = ZipCodeManager()
    for c in country_list:
        zc_manager.add(c)
        for zc, data in zc_manager.zipcodes(c).items():
            sender.ZipCode.objects.get_or_create(zipcode=zc, city=data['city'], state=data['state'], country=c)

post_syncdb.connect(save_zipcodes, sender=zipcodes.models)
