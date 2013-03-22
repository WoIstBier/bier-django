from models import Kiosk, Image, Beer, KioskImage
from rest_framework import serializers
from pygeocoder import Geocoder


class KioskSerializer(serializers.ModelSerializer):
    exists = False
    def save(self):
        k = self.object
        #address = "%s %s, %s, Deutschland" % (k.street, k.number, k.city)
        #result = Geocoder.geocode(address)
        # chekc if address is valid and add street name from google to get rid of spelling differences
        k.save(commit=False)
        
        if k.is_valid_address:
            ks = Kiosk.objects.all().filter(street = k.street, number= k.number);
            if ks.exists() :
                self.double_entry = True
                return
            self.object.save()
            

    class Meta:
        model = Kiosk
        

class ImageSerializer(serializers.ModelSerializer):
    imageUrl = serializers.CharField(source='image.url', read_only=True)
    thumbUrl = serializers.CharField(source='thumbnail.url', read_only=True)
    
#    def validate(self, attrs):
#        if self.context.get('kiosk_id') is None:
#            raise serializers.ValidationError("no kiosk id provided for this image. jerk!")
#        return attrs
    
#    def save(self):
##            super(ImageSerializer, self).save()  
#            request = self.context.get('request') 
#            imgModel = Image(image=request.FILES['image'], thumbnail=None)
#            imgModel.save()
##            tu = self.fields.get('thumbUrl')
##             
##            self.fields.insert(2,'thumbUrl' , serializers.CharField(source='thumbnail.url', read_only=True))
#            kiosk_id = self.context.get('kiosk_id')
#            k = KioskImage(kiosk = Kiosk.objects.get(pk=kiosk_id) , img=imgModel)
#            k.save()
            
    class Meta:
        model = Image
        
class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        