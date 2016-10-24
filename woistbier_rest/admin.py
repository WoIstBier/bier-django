# -*- coding: utf-8 -*-
'''
Created on Feb 17, 2013

@author: mackaiver
'''
from django.contrib import admin
from django.core.urlresolvers import reverse
#from polls.models import Poll, Choice
from woistbier_rest.models import Kiosk, Beer, BeerPrice, Image, Comment
from pygeocoder import Geocoder
import logging
log = logging.getLogger(__name__)

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class BeerPriceInline(admin.TabularInline):
    model = BeerPrice
    extra = 2

class CommentInline(admin.TabularInline):
    model = Comment
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
     (None, {'fields': ['geo_long']}), 
     (None, {'fields': ['is_valid_address']}),
     (None, {'fields': ['description']})    
     
    ]
    inlines = [BeerPriceInline, CommentInline, ImageInline]
    actions = ['get_geo_information_action']

        
    def get_geo_information(self, obj):
        if obj.is_valid_address:
            return 0
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
            return 0
        # chekc if address is valid and add street name from google to get rid of spelling differences
        obj.is_valid_address = location[0].valid_address
        if (obj.is_valid_address):
            obj.street = location[0].route
            obj.city = location[0].locality    
            #self.city = location[0].city
            # add zip code
            obj.zip_code = location[0].postal_code
            (obj.geo_lat, obj.geo_long) = location[0].coordinates
            # in case name is not set. generate it
            if obj.name == '' or obj.name is None:
                obj.name = obj.street + ' ' + str(obj.number);
            log.info("Creating new Kiosk: %s" % obj.name )
#         # custom stuff here
        obj.save()
        return 1
    
    def get_geo_information_action(self, request, queryset):
        i = 0
        for obj in queryset:
            i += self.get_geo_information(obj)
        self.message_user(request, "%s kioske successfully updated." % i)
    get_geo_information_action.short_description = "Update geo infos from google"
            
    def save_model(self, request, obj, form, change):
        self.get_geo_information(obj)
    
class BeerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name. z.B. Hansa Pils',               {'fields': ['name']}),
        ('Marke bzw. Brauerei z.B. Hansa', {'fields': ['brand']}),
        ('Heimat des Bieres',   {'fields': ['location']}),
        ('Sorte des Bieres z.B. Weizen',   {'fields': ['brew']}),
    ]
    list_display = ('brand', 'name', 'brew', 'location')
    model = Beer
    


class KioskForeign(admin.ModelAdmin):
    """ Meta View for all Views, containing a foreign key to kiosk.
    """

    def link_to_kiosk(self, obj):
        """ Creates a link to a kiosk admin view
        """
        link = reverse("admin:woistbier_rest_kiosk_change",
                       args=[obj.kiosk.id])
        return '<a href="{}">{}</a>'.format(link, obj.kiosk.name)

    link_to_kiosk.allow_tags = True


class BeerPriceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Bier. z.B. Hansa Pils',               {'fields': ['beer']}),
        ('Preis',   {'fields': ['price']}),
        ('FlaschenGröße',   {'fields': ['size']}),
        ('Preis pro liter',   {'fields': ['score']}),
    ]
    list_display = ('beer', 'price', 'size', 'score')
    model = BeerPrice
    
    actions = ['calc_scores']
    
    def calc_scores(self, request, queryset):
        i = 0
        for obj in queryset:
            i += self.calculate_score(obj)
        self.message_user(request, "%s kioske successfully updated." % i)

    calc_scores.short_description = "Update geo infos from google"
    
    def calculate_score(self, obj):
        if obj.score == 0:
            obj.score = obj.price / obj.size
            obj.save()
            return 1
        return 0
    
# class KioskImageAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Kiosk',               {'fields': ['kiosk']}),
#         ('Bild', {'fields': ['image']})
#     ]
#     list_display = ('kiosk', 'image')
#    inlines = [ImageInline]


class ImageAdmin(KioskForeign):
    list_display = ['admin_img', 'image', 'link_to_kiosk']
    fields = ['image', 'link_to_kiosk']
    readonly_fields = ['link_to_kiosk']
    model = Image


class CommentAdmin(KioskForeign):
    list_display = ['name', 'comment', 'link_to_kiosk']
    fields = list_display
    readonly_fields = ['link_to_kiosk']
    model = Comment


admin.site.register(Image, ImageAdmin)
admin.site.register(Comment, CommentAdmin)
#admin.site.register(KioskImage, KioskImageAdmin)
admin.site.register(Kiosk, KioskAdmin)
admin.site.register(Beer, BeerAdmin)
admin.site.register(BeerPrice, BeerPriceAdmin)
