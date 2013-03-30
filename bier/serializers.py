# -*- coding: utf-8 -*-
from models import Kiosk, Image, Beer, Comment, BeerPrice
from rest_framework import serializers


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
    name = serializers.CharField(source='beer.name', read_only=True)
    location = serializers.CharField(source='beer.location', read_only=True)
    brand= serializers.CharField(source='beer.brand', read_only=True)
    class Meta:
        model = BeerPrice 
        fields = ('price', 'size', 'name', 'brand', 'location') 