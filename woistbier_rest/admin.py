# -*- coding: utf-8 -*-
'''
Created on Feb 17, 2013

@author: mackaiver
'''
from django.contrib import admin
from django.core.urlresolvers import reverse
from woistbier_rest.models import Kiosk, Beer, BeerPrice, Image, Comment
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


class BeerPriceAdmin(KioskForeign):
    fieldsets = [
        ('Bier. z.B. Hansa Pils',               {'fields': ['beer']}),
        ('Preis',   {'fields': ['price']}),
        ('FlaschenGröße',   {'fields': ['size']}),
        ('Preis pro liter',   {'fields': ['score']}),
        ('Kiosk', {'fields': ['link_to_kiosk']}),
    ]
    list_display = ('beer', 'price', 'size', 'score', 'link_to_kiosk')
    readonly_fields = ['link_to_kiosk']
    model = BeerPrice


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
admin.site.register(Kiosk, KioskAdmin)
admin.site.register(Beer, BeerAdmin)
admin.site.register(BeerPrice, BeerPriceAdmin)
