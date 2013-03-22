# -*- coding: utf-8 -*-
from django.db import models
#from geopy import geocoders
from django.forms import forms, ModelForm
from django.core.files.base import ContentFile
from django.core.files import File
from pygeocoder import Geocoder
import datetime
import os.path
# Create your models here.
class Kiosk(models.Model):
    street = models.CharField('street_name', max_length=150)
    number = models.CharField('building_number', max_length=3)
    zip_code = models.CharField(max_length=6, blank=True, null=True)
    city = models.CharField(max_length=30)
    name = models.CharField('kiosk_name', max_length=160, blank=True)
    owner = models.CharField('owners_name', max_length=100, blank=True, null=True)
    geo_lat = models.DecimalField('latitude', max_digits=13, decimal_places=10, blank=True, null=True)
    geo_long = models.DecimalField('longitude', max_digits=13, decimal_places=10, blank=True, null=True)
    is_valid_address = models.BooleanField('google_says_valid', default=False )
    doubleEntry= False
    
    def __unicode__(self):
        return self.name
    
    def save(self):
        address = "%s %s, %s, Deutschland" % (self.street, self.number, self.city)
        try:
            location = Geocoder.geocode(address)
        except Exception, e:
            self.is_valid_address = False
            return self
        # chekc if address is valid and add street name from google to get rid of spelling differences
        self.is_valid_address = location[0].valid_address
        if (self.is_valid_address):
            self.street = location[0].route
            self.city = location[0].locality    
            q = Kiosk.objects.all().filter(street = self.street, number  = self.number, city= self.city)
            if q.exists():
                self.doubleEntry=True
                return self
            #self.city = location[0].city
            # add zip code
            self.zip_code = location[0].postal_code
            (self.geo_lat, self.geo_long) = location[0].coordinates
            # in case name is not set. generate it
            if self.name == '' or self.name is None:
                self.name = self.street + ' ' + str(self.number);

            return super(Kiosk, self).save() # Call the "real" save() method
        else:
            return self
        

class Beer(models.Model):
    BREW_CHOICES = (
        ('pils', 'Pils'),
        ('export', 'Export'),
        ('weizen', 'Weizen'),
        ('dunkel', 'Dunkel'),
        ('export', 'Hell'),
        ('lager', 'Lager'),
        ('koelsch', 'Kölsch')
    )
    brew = models.CharField(max_length=20, choices=BREW_CHOICES, default='pils')
    name  = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
    
class BeerPrice(models.Model):
    KLEIN = 0.33
    NORMAL = 0.5
    SIZE_CHOICES = (
        (0.25, 'belgisch klein 0.25'),
        (0.33, 'klein 0.33'),
        (0.375, 'lambic 0.33'),
        (0.5, 'normal 0.5'),
        (0.5, 'italien normal 0.5'),
        (0.7, 'suedasien 0.7'),
        (0.8, 'australien groß 0.8'),
        (1.0, 'groß 1.0'),
    )
    size = models.FloatField(max_length=1, choices=SIZE_CHOICES, default = NORMAL )
    kiosk = models.ForeignKey(Kiosk)
    beer = models.ForeignKey(Beer)
    price = models.IntegerField()
    created = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified = models.DateTimeField(auto_now = True, blank=True, null=True)
    
    def save(self):
#        if self.pk is None:
#            self.created = datetime.datetime.today()
#        self.modified = datetime.datetime.today()
        if self.size is None:
            self.size = 0.5
        super(BeerPrice, self).save()
    
    def __unicode__(self):
        return str(self.price)

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
        blank=True
    )
    #display image in admin view with this function
    def admin_img(self):
        if self.image:
            return u'<img src="%s" alt="Bild" />' % self.thumbnail.url
        else:
            return 'no image. WTF'
    
    admin_img.short_description = 'Thumb'
    admin_img.allow_tags = True
        
    
    
    def __unicode__(self):
        return self.image.name
     
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

''' This model connects images with kiosks'''
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
    def __unicode__(self):
        return self.image.path
    