from models import Kiosk, Image
from rest_framework import serializers


class KioskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiosk
        

class ImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.CharField(source='image.url', read_only=True)
    thumbUrl = serializers.CharField(source='thumbnail.url', read_only=True)
    class Meta:
        model = Image
        
