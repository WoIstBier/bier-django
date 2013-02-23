'''
Created on Feb 17, 2013

@author: mackaiver
'''
from django.contrib import admin
#from polls.models import Poll, Choice
from bier.models import Kiosk, Beer, BeerPrice

class BeerPriceInline(admin.TabularInline):
    model = BeerPrice
    extra = 2

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
    inlines = [BeerPriceInline]
    
admin.site.register(Kiosk, KioskAdmin)
