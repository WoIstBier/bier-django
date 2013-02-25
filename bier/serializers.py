from models import Kiosk
from rest_framework import serializers
class KioskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiosk
        fields = ('id', 'name', 'street', 'number', 'zip_code', 'city', 'owner', 'geo_lat', 'geo_long')

