# -*- coding: utf-8 -*-
from django.db import models
#from geopy import geocoders
from django.forms import forms
from easy_thumbnails.fields import ThumbnailerImageField
import logging
log = logging.getLogger(__name__)

'''Model for a Kiosk. 
zip_code, geo info and valid addres flag will be supplied by the client with a google lookup
There is a custom save method in the admin model in case a kiosk will be saved from the admin page
'''
class Kiosk(models.Model):
    street = models.CharField('street_name', max_length=150)
    number = models.IntegerField('building_number') 
    zip_code = models.CharField(max_length=6, blank=True, null=True)
    city = models.CharField(max_length=30)
    name = models.CharField('kiosk_name', max_length=160, blank=True)
    description = models.CharField('description', max_length=600, blank=True, null = True)
    owner = models.CharField('owners_name', max_length=100, blank=True, null=True)
    geo_lat = models.DecimalField('latitude', max_digits=13, decimal_places=10, blank=True, null=True)
    geo_long = models.DecimalField('longitude', max_digits=13, decimal_places=10, blank=True, null=True)
    is_valid_address = models.BooleanField('google_says_valid', default=False )
    created = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    
    '''Custom save method to create a name for the kiosk if no name was supplied'''
    def save(self, *args, **kwargs):
        if self.name == '' or self.name is None:
                self.name = self.street + ' ' + str(self.number);
        super(Kiosk, self).save(*args, **kwargs);

    class Meta:
        unique_together = ("city","street", "number", "zip_code")
#     doubleEntry=False

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
    
class Comment(models.Model):
    name = models.CharField(max_length=25, default='Anonymer Alkoholiker')
    comment = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    kiosk = models.ForeignKey(Kiosk)

    def __unicode__(self):
        return self.name+str(self.created)

''' 
This class connects beers with kiosks and add information about pricing and aisze of the bottle
the score field is basicly cents per liter which makes it possible to find the cheapest beer per liter
'''
class BeerPrice(models.Model):
    KLEIN = 0.33
    NORMAL = 0.5
    SIZE_CHOICES = (
        (0.25, 'belgisch klein 0.25'),
        (0.33, 'klein 0.33'),
        (0.375, 'lambic 0.375'),
        (0.5, 'normal 0.5'),
        (0.6, 'italien normal 0.6'),
        (0.7, 'suedasien 0.7'),
        (0.8, 'australien groß 0.8'),
        (1.0, 'groß 1.0'),
    )
    size = models.FloatField(max_length=1, choices=SIZE_CHOICES, default = NORMAL )
    kiosk = models.ForeignKey(Kiosk, related_name='related_kiosk')
    beer = models.ForeignKey(Beer, related_name='related_beer')
    price = models.IntegerField()
    score = models.FloatField(max_length=1, default = 1 )
    created = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    modified = models.DateTimeField(auto_now = True, blank=True, null=True)
    class Meta:
        unique_together = ("beer","kiosk", "size")
    
    def save(self,*args, **kwargs):
        self.score = self.price / self.size
        super(BeerPrice, self).save(*args, **kwargs) # Call the "real" save() method
        
    
    def __unicode__(self):
        return str(self.price)

'''
Model containing an image which automaticly creates a thumbnail when imagesize > maxSize
'''
class Image(models.Model):
    image = ThumbnailerImageField(upload_to='images/',  max_length=300,  blank=True)
    kiosk = models.ForeignKey(Kiosk)
    
    #display image in admin view with this function
    def admin_img(self):
        if self.image:
            return u'<image src="%s" alt="Bild" />' % self.image['medium'].url
        else:
            return 'no image. WTF'
    
    admin_img.short_description = 'Thumb'
    admin_img.allow_tags = True
        
    
    
    def __unicode__(self):
        return self.image.name
     
#     def create_thumbnail(self):
#         from PIL import Image
# #        print('HALLO PFAD:: ' + self.image.path  + '  url:  ' + self.image.url + '  name: ' + self.image.name)
#         imgFile = Image.open(self.image)
#         #Convert to RGB
#         if imgFile.mode not in ('L', 'RGB'):
#             imgFile = imgFile.convert('RGB')
#         # get path to thumbFile
#         thumb_path = self.get_default_thumbnail_filename(self.image.path)
#         imgFile = imgFile.copy()
#         # if picture is too big create a thumbnail 
#         if imgFile.size[0] > self.maxWidth or imgFile.size[1] > self.maxHeight:
#             imgFile.thumbnail((self.maxWidth,self.maxHeight), Image.ANTIALIAS)
# #        print('Saving to:  ' + thumb_path)
#         imgFile.save(thumb_path, 'JPEG', qualitiy=95)
#         f = open(thumb_path)
#         myfile = File(f)
# #       save thumbnail to thumbnail field but dont call the save method again. or youl get a inifinite save loop ya know 
#         self.thumbnail.save(thumb_path, myfile, save=False )
    
#     def get_default_thumbnail_filename(self, filename):
#         path, full_name = os.path.split(filename)
#         name, ext = os.path.splitext(full_name)
#         return path + '/images/thumbs/' + name + '_thumb' + ext
# 
#     def save(self, *args, **kwargs):
#         self.create_thumbnail()
#         force_update = False
#         # If the instance already has been saved, it has an id and we set
#         # force_update to True
#         if self.id:
#             force_update = True
#         # Force an UPDATE SQL query if we're editing the image to avoid integrity exception
#         super(Image, self).save(force_update=force_update)

# ''' This model connects images with kiosks'''
# class KioskImage(models.Model):
#     kiosk = models.ForeignKey(Kiosk)
#     image = models.ForeignKey(Image, null=False)
#     
#     def __unicode__(self):
#         return self.kiosk.name 

# ''' This model connects images with kiosks'''
# class KioskComments(models.Model):
#     kiosk = models.ForeignKey(Kiosk)
#     comment = models.ForeignKey(Comment)
#     
#     def __unicode__(self):
#         return self.kiosk.name + self.comment.name

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
    