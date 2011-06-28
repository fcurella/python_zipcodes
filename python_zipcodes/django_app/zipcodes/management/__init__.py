from python_zipcodes.django_app.zipcodes import models
from python_zipcodes.django_app.zipcodes.signals import save_zipcodes
from django.db.models.signals import post_syncdb

post_syncdb.connect(save_zipcodes, sender=models)
