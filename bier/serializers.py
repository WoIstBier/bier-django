# -*- coding: utf-8 -*-
from models import Kiosk, Image, Beer, Comment, BeerPrice
from rest_framework import serializers

import logging
log = logging.getLogger(__name__)


class KioskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiosk
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment

class ImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.CharField(source='image.url', read_only=True)
    thumbUrl = serializers.CharField(source='thumbnail.url', read_only=True)
    
    class Meta:
        model = Image



class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        
        
class BeerPriceSerializer(serializers.ModelSerializer):
    beer_name = serializers.CharField(source='beer.name', read_only=True)
    beer_location = serializers.CharField(source='beer.location', read_only=True)
    beer_brand= serializers.CharField(source='beer.brand', read_only=True)
    
#     def restore_object(self, attrs, instance=None):
#         """
#         Create or update a new snippet instance, given a dictionary
#         of deserialized field values.
# 
#         Note that if we don't define this method, then deserializing
#         data will simply return a dictionary of items.
#         """
#         if instance:
#             # Update existing instance
#             log.warn("BeerPriceSerializer tries to update an instance. Ok so far.")
# #             instance.title = attrs.get('title', instance.title)
# #             instance.code = attrs.get('code', instance.code)
# #             instance.linenos = attrs.get('linenos', instance.linenos)
# #             instance.language = attrs.get('language', instance.language)
# #             instance.style = attrs.get('style', instance.style)
# #             return instance
# 
#         # Create new instance
#         return BeerPrice(**attrs)
    
    
    class Meta:
        model = BeerPrice 
