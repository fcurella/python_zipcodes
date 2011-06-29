from django.core.management.base import BaseCommand, CommandError
from python_zipcodes.django_app.zipcodes.models import ZipCode
from python_zipcodes.countries import country_list
from python_zipcodes.importers import ZipCodeManager
from python_zipcodes.django_app.zipcodes.signals import save_zipcodes

class Command(BaseCommand):
    args = ''
    help = 'Updates the zip codes'

    def handle(self, *args, **options):
        ZipCode.objects.all().delete()
        save_zipcodes()