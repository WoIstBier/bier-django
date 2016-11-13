# -*- coding: utf-8 -*-
from woistbier_rest.models import Kiosk, Image, Beer, Comment, BeerPrice
from rest_framework import serializers

import logging
log = logging.getLogger(__name__)


class KioskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiosk
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=300, allow_empty_file=True)

    medium_url = serializers.ReadOnlyField(source='get_medium_url')
    gallery_url = serializers.ReadOnlyField(source='get_gallery_url')
    thumbnail_url = serializers.ReadOnlyField(source='get_thumbnail_url')
#     kiosk = serializers.IntegerField(read_only=True)
    class Meta:
        model = Image
        fields='__all__'


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = '__all__'

class BeerPriceSerializer(serializers.ModelSerializer):
    beer_name = serializers.CharField(source='beer.name', read_only=True)
    beer_location = serializers.CharField(source='beer.location', read_only=True)
    beer_brand= serializers.CharField(source='beer.brand', read_only=True)

    class Meta:
        model = BeerPrice
        fields = '__all__'

class KioskDetailSerializer(serializers.Serializer):
    images = ImageSerializer(many=True)
    beerPrices = BeerPriceSerializer(source='beerPrice', many=True)
    comments = CommentSerializer( many=True)
    kiosk = KioskSerializer()
    comment_count = serializers.IntegerField(read_only=True)
    beer_count = serializers.IntegerField( read_only=True)
    average_price = serializers.IntegerField(source='avg_price.score__avg', read_only=True)


'''
Non-Modell Serializer
We dont need to restore objects since this is a read only serializer
'''
class KioskListItemSerializer(serializers.Serializer):
#     kioskId = serializers.IntegerField(source='kiosk.id', read_only=True)
#     kioskName = serializers.CharField(source='kiosk.name', read_only=True)
#     kioskStreet = serializers.CharField(source='kiosk.street', read_only=True)
#     kioskCity = serializers.CharField(source='kiosk.city', read_only=True)
#     kioskPostalCode = serializers.IntegerField(source='kiosk.zip_code', read_only=True)
#     kioskLatitude = serializers.IntegerField(source='kiosk.geo_lat', read_only=True)
#     kioskLongtitude = serializers.IntegerField(source='kiosk.geo_long', read_only=True)
#     kioskNumber = serializers.IntegerField(source='kiosk.number', read_only=True)
#     beerName = serializers.CharField(source='beerPrice.beer.name', read_only=True)
#     beerBrew = serializers.CharField(source='beerPrice.beer.brew', read_only=True)
#     beerSize = serializers.FloatField(source='beerPrice.size', read_only=True)
#     beerPrice = serializers.IntegerField(source='beerPrice.price', read_only=True)
#     thumb_path = serializers.CharField(source='thumb', read_only=True)
    distance = serializers.FloatField(read_only=True)
    kiosk = KioskSerializer()
    image = ImageSerializer()
    beerPrice = BeerPriceSerializer()

#     thumb = ImageSerializer()
