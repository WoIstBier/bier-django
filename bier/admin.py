'''
Created on Feb 17, 2013

@author: mackaiver
'''
from django.contrib import admin
#from polls.models import Poll, Choice
from bier.models import Kiosk, Beer, BeerPrice, KioskImage, Image

class ImageInline(admin.TabularInline):
    model = Image

class BeerPriceInline(admin.TabularInline):
    
    model = BeerPrice
    extra = 2

class KioskImageInline(admin.TabularInline):
    model = KioskImage
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
     (None, {'fields': ['geo_long']})  
    ]
    inlines = [BeerPriceInline, KioskImageInline]
    
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
        ('Bild', {'fields': ['img']})
    ]
    list_display = ('kiosk', 'img')
#    inlines = [ImageInline]
    
class ImageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Bild',               {'fields': ['image']}),
        ('Kleines Bild. (wird automatisch generiert)', {'fields': ['thumbnail']})
    ]
    list_display = ('admin_img', 'image')
    model = Image

admin.site.register(Image, ImageAdmin)
#admin.site.register(KioskImage, KioskImageAdmin)
admin.site.register(Kiosk, KioskAdmin)
admin.site.register(Beer, BeerAdmin)