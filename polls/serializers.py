from models import Kiosk
from rest_framework import serializers
class KioskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiosk
        fields = ('id', 'name', 'addres', 'owner')