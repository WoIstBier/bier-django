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

class ImageOutputSerializer(serializers.Serializer):
    imageUrl = serializers.CharField(source='url.get(thumbnail_url)', read_only=True)
    thumbUrl = serializers.CharField(source='url.get(thumbnail_url)', read_only=True)
    mediumUrl = serializers.CharField(source='url.get(thumbnail_url)', read_only=True)
    kioskId = serializers.IntegerField(source='url.get(kiosk_id)', read_only=True)

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=300, allow_empty_file=False)
#     kiosk = serializers.IntegerField(read_only=True)
    class Meta:
        model = Image


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer



class BeerPriceSerializer(serializers.ModelSerializer):
    beer_name = serializers.CharField(source='beer.name', read_only=True)
    beer_location = serializers.CharField(source='beer.location', read_only=True)
    beer_brand= serializers.CharField(source='beer.brand', read_only=True)
    
    class Meta:
        model = BeerPrice 

class KioskDetailSerializer(serializers.Serializer):
    images = ImageSerializer(source='images', many=True)
    beerPrices = BeerPriceSerializer(source='beerPrice', many=True)
    comments = CommentSerializer(source='comments', many=True)
    kiosk = KioskSerializer(source='kiosk')
    

'''
Non-Modell Serializer
We dont need to restore objects since this is a read only serializer
'''
class KioskListItemSerializer(serializers.Serializer):
    kioskId = serializers.IntegerField(source='kiosk.id', read_only=True)
    kioskName = serializers.CharField(source='kiosk.name', read_only=True)
    kioskStreet = serializers.CharField(source='kiosk.street', read_only=True)
    kioskCity = serializers.CharField(source='kiosk.city', read_only=True)
    kioskPostalCode = serializers.IntegerField(source='kiosk.zip_code', read_only=True)
    kioskLatitude = serializers.IntegerField(source='kiosk.geo_lat', read_only=True) 
    kioskLongtitude = serializers.IntegerField(source='kiosk.geo_long', read_only=True)
    kioskNumber = serializers.IntegerField(source='kiosk.number', read_only=True) 
    beerName = serializers.CharField(source='beerPrice.beer.name', read_only=True)
    beerBrew = serializers.CharField(source='beerPrice.beer.brew', read_only=True)
    beerSize = serializers.FloatField(source='beerPrice.size', read_only=True)
    beerPrice = serializers.IntegerField(source='beerPrice.price', read_only=True)
    thumb_path = serializers.CharField(source='thumb', read_only=True)
    distance = serializers.FloatField(source='distance', read_only=True)
#     kiosk = KioskSerializer(source='kiosk')
#     image = ImageSerializer(source='thumb')
#     beerPrice = BeerPriceSerializer(source='beerPrice')
    
#     thumb = ImageSerializer()
    
