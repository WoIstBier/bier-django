from django.db import models
from geopy import geocoders
from django.forms import forms, ModelForm
from django.core.files.base import ContentFile
from django.core.files import File
import datetime
import os.path
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
    
    def save(self):
        add = "%s, %s, %s, %s" % (self.street, self.number , self.zip_code, self.city)
        g = geocoders.Google()
        place , (self.geo_lat, self.geo_long) = g.geocode(add)
        super(Kiosk, self).save() # Call the "real" save() method

class Beer(models.Model):
    name  = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
    
class BeerPrice(models.Model):
    kiosk = models.ForeignKey(Kiosk)
    beer = models.ForeignKey(Beer)
    price = models.IntegerField()
    created = models.DateTimeField()
    modified = models.DateTimeField()
    
    def save(self):
        if self.pk is None:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(BeerPrice, self).save()
    
    def __unicode__(self):
        return self.price

'''
Model containing an image which automaticly creates a thumbnail when imagesize > maxSize
'''
class Image(models.Model):
    maxWidth = 150;
    maxHeight = 150;
    
    image = models.ImageField(
        upload_to='images/',
        max_length=500,
        blank=True
    )
     
    thumbnail = models.ImageField(
        upload_to='images/thumbs/',
        max_length=500,
        null=True,
        blank=True
    )
     
    def create_thumbnail(self):
        from PIL import Image
#        print('HALLO PFAD:: ' + self.image.path  + '  url:  ' + self.image.url + '  name: ' + self.image.name)
        imgFile = Image.open(self.image)
        #Convert to RGB
        if imgFile.mode not in ('L', 'RGB'):
            imgFile = imgFile.convert('RGB')
        # get path to thumbFile
        thumb_path = self.get_default_thumbnail_filename(self.image.path)
        imgFile = imgFile.copy()
        # if picture is too big create a thumbnail 
        if imgFile.size[0] > self.maxWidth or imgFile.size[1] > self.maxHeight:
            imgFile.thumbnail((self.maxWidth,self.maxHeight), Image.ANTIALIAS)
#        print('Saving to:  ' + thumb_path)
        imgFile.save(thumb_path, 'JPEG', qualitiy=95)
        f = open(thumb_path)
        myfile = File(f)
#       save thumbnail to thumbnail field but dont call the save method again. or youl get a inifinite save loop ya know 
        self.thumbnail.save(thumb_path, myfile, save=False )
    
    def get_default_thumbnail_filename(self, filename):
        path, full_name = os.path.split(filename)
        name, ext = os.path.splitext(full_name)
        return path + '/images/thumbs/' + name + '_thumb' + ext

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        force_update = False
        # If the instance already has been saved, it has an id and we set
        # force_update to True
        if self.id:
            force_update = True
        # Force an UPDATE SQL query if we're editing the image to avoid integrity exception
        super(Image, self).save(force_update=force_update)


class KioskImage(models.Model):
    kiosk = models.ForeignKey(Kiosk)
    img = models.ForeignKey(Image)
    
    def __unicode__(self):
        return self.kiosk.name + self.img.image.path

#class ImageForm(ModelForm):
#    class Meta:
#        model = Image


class ImageForm(forms.Form):
    image = forms.FileField(
        label='Waehle ein bild von deinem Computer',
        help_text='max. 2.5 megabytes'
    )