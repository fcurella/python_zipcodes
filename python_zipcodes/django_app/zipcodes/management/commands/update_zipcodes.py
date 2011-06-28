from django.core.management.base import BaseCommand, CommandError
from python_zipcodes.django_app.zipcodes.models import ZipCode
from python_zipcodes.countries import country_list
from python_zipcodes.importers import ZipCodeManager

class Command(BaseCommand):
    args = '
    help = 'Updates the zip codes'

    def handle(self, *args, **options):
        zc_manager = ZipCodeManager()
        for c in country_list:
            zc_manager.add(c)
            for zc, data in zc_manager.zipcodes(c).items():
                ZipCode.objects.get(zipcode=zc, country=c).delete()
                ZipCode.objects.create(zipcode=zc, city=data['city'], state=data['state'], country=c)
