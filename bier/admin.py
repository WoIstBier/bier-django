'''
Created on Feb 17, 2013

@author: mackaiver
'''
from django.contrib import admin
#from polls.models import Poll, Choice
from bier.models import Kiosk, BeerPrice

class BierPreisListeInline(admin.TabularInline):
    model = BeerPrice
    extra = 2

class KioskAdmin(admin.ModelAdmin):
    fieldsets = [
     (None, {'fields': ['name']}),
        (None, {'fields': ['address']}),
    ]
    inlines = [BierPreisListeInline]
    
admin.site.register(Kiosk, KioskAdmin)
