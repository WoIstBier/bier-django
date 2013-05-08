# -*- coding: utf-8 -*-
'''
Created on Feb 17, 2013

@author: mackaiver
'''
from django.contrib import admin
#from polls.models import Poll, Choice
from bier.models import Kiosk, Beer, BeerPrice, KioskImage, Image, KioskComments, Comment
from pygeocoder import Geocoder
import logging
log = logging.getLogger(__name__)

class ImageInline(admin.TabularInline):
    model = Image

class BeerPriceInline(admin.TabularInline):
    model = BeerPrice
    extra = 2

class KioskImageInline(admin.TabularInline):
    model = KioskImage
    extra = 1
    
class KioskCommentInline(admin.TabularInline):
    model = KioskComments
    extra = 1
    
    
class KioskAdmin(admin.ModelAdmin):
    fieldsets = [
     (None, {'fields': ['name']}),
     (None, {'fields': ['street']}),
     (None, {'fields': ['number']}),
     (None, {'fields': ['zip_code']}),
     (None, {'fields': ['city']}),
     (None, {'fields': ['owner']}), 
     (None, {'fields': ['geo_lat']}),
     (None, {'fields': ['geo_long']}), 
     (None, {'fields': ['is_valid_address']}),
     (None, {'fields': ['description']})    
     
    ]
    inlines = [BeerPriceInline, KioskImageInline, KioskCommentInline]
    
    def save_model(self, request, obj, form, change):
        address = "%s %s, %s, Deutschland" % (obj.street, obj.number, obj.city)
        address = address.replace(unicode('ä',"utf-8"), "ae")
        address = address.replace(unicode('ö',"utf-8"), "oe")
        address = address.replace(unicode('ü',"utf-8"), "ue")
        address = address.replace(unicode('ß',"utf-8"), "ss")
        try:
            location = Geocoder.geocode(address)
        except Exception:
            obj.is_valid_address = False
            log.info("Google did not return any results for %s" % address )
            return None
        # chekc if address is valid and add street name from google to get rid of spelling differences
        obj.is_valid_address = location[0].valid_address
        if (obj.is_valid_address):
            obj.street = location[0].route
            obj.city = location[0].locality    
#             q = Kiosk.objects.all().filter(street = self.street, number  = self.number, city= self.city)
#             if q.exists():
#                 self.doubleEntry=True
#                 log.info("Someone tried to add an existing kiosk: %s" % address )
#                 return None
#             self.doubleEntry = False
            #self.city = location[0].city
            # add zip code
            obj.zip_code = location[0].postal_code
            (obj.geo_lat, obj.geo_long) = location[0].coordinates
            # in case name is not set. generate it
            if obj.name == '' or obj.name is None:
                obj.name = obj.street + ' ' + str(obj.number);
            log.info("Creating new Kiosk: %s" % obj.name )
#             return obj.save() # Call the "real" save() method
#         # custom stuff here
        obj.save()
    
class BeerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name. z.B. Hansa Pils',               {'fields': ['name']}),
        ('Marke bzw. Brauerei z.B. Hansa', {'fields': ['brand']}),
        ('Heimat des Bieres',   {'fields': ['location']}),
        ('Sorte des Bieres z.B. Weizen',   {'fields': ['brew']}),
    ]
    list_display = ('brand', 'name', 'brew', 'location')
    
class KioskImageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Kiosk',               {'fields': ['kiosk']}),
        ('Bild', {'fields': ['image']})
    ]
    list_display = ('kiosk', 'image')
#    inlines = [ImageInline]
    
class ImageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Bild',               {'fields': ['image']}),
        ('Kleines Bild. (wird automatisch generiert)', {'fields': ['thumbnail']})
    ]
    list_display = ('admin_img', 'image')
    model = Image
    
class CommentAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Name des Autors',               {'fields': ['name']}),
#         ('Erstellungsdatum', {'fields': ['created']}),
#         ('Text', {'fields': ['comment']})
#     ]
    fields = ['name', 'comment']
#     list_display = ('name', 'created', 'comment')
    model = Comment

admin.site.register(Image, ImageAdmin)
admin.site.register(Comment, CommentAdmin)
#admin.site.register(KioskImage, KioskImageAdmin)
admin.site.register(Kiosk, KioskAdmin)
admin.site.register(Beer, BeerAdmin)