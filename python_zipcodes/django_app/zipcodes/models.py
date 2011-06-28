from django.db import models
# Create your models here.
class ZipCode(models.Model):
    """(ZipCode description)"""
    zipcode = models.CharField(blank=False, max_length=100)
    country = models.CharField(blank=False, max_length=2)
    city = models.CharField(blank=False, max_length=255)
    state = models.CharField(blank=False, max_length=255)

    class Meta:
        unique_together = ('zipcode', 'country')

    def __unicode__(self):
        return u"%s: %s, %s - %s" % (self.zipcode, self.city, self.state, self.country,)

