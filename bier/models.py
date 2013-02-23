from django.db import models

# Create your models here.
class Kiosk(models.Model):
    street = models.CharField('street_name', max_length=100)
    number = models.CharField('building_number', max_length=3)
    zip_code = models.CharField(max_length=6)
    city = models.CharField(max_length=30)
    name = models.CharField('kiosk_name', max_length=100)
    owner = models.CharField('owners_name', max_length=100)
    geo_lat = models.DecimalField('latitude', max_digits=13, decimal_places=10, blank=True, null=True)
    geo_long = models.DecimalField('longitude', max_digits=13, decimal_places=10, blank=True, null=True)
    
    def __unicode__(self):
        return self.name

class BeerPrice(models.Model):
    kiosk = models.ForeignKey(Kiosk)
    beer = models.ForeignKey(Beer)
    price = models.IntegerField()
    date = models.DateTimeField();
    def __unicode__(self):
        return self.price

class Beer(models.Model):
    name  = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name