from django.db import models

# Create your models here.
class Kiosk(models.Model):
    address = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class BierPreisListe(models.Model):
    kiosk = models.ForeignKey(Kiosk)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    date = models.DateTimeField();
    def __unicode__(self):
        return self.name