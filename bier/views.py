# -*- coding: utf-8 -*-
# Create your views here.
from bier.models import Kiosk, BeerPrice, Image, Beer, Comment
from bier.serializers import KioskSerializer, ImageSerializer, BeerSerializer, CommentSerializer, BeerPriceSerializer, KioskListItemSerializer, KioskDetailSerializer
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render_to_response
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import math
import logging
log = logging.getLogger(__name__)



def index(request):
    return render_to_response('bier/index.html')

def kiosk(request):
    kiosk_liste = Kiosk.objects.order_by('name')
    return render_to_response('bier/kiosk.html', {'kioske': kiosk_liste })

'''
Here come the views for the rest api
'''

''' Some helper Functions'''
def check_kiosk_args(kiosk_id):
    if kiosk_id == None:
        return False
    try:
        long(kiosk_id)
    except ValueError:
        return False
    return True
    
def check_if_kiosk_exists(kiosk_id):
    try:
        Kiosk.objects.get(pk = kiosk_id)
    except Kiosk.DoesNotExist:
        return False
    return True

def getSetForKioskId(model, serializer, kiosk_id):
    if kiosk_id is None:
            commentSet = model.objects.all()
    else: 
            if not check_kiosk_args(kiosk_id):
                return HttpResponseBadRequest("Kiosk id arguments was malformed")
    
            commentSet = model.objects.filter(kiosk__pk = kiosk_id)
            if commentSet.count()== 0:
                return Response(status = status.HTTP_204_NO_CONTENT)
    serializer = serializer(commentSet, many=True)
    return Response(serializer.data)  
    
    
''' views for images'''
class ImageList(APIView):
    
    def get(self, request):
        kiosk_id = self.request.QUERY_PARAMS.get('kiosk', None)
        return getSetForKioskId(Image, ImageSerializer, kiosk_id)
    
    def post(self, request):
        #curl -X POST -S -H 'Accept: application/json' -F "image=@/home/mackaiver/Pictures/alf2.jpg; type=image/jpg" http://localhost:8000/bier/rest/image/68/
        serializer = ImageSerializer(data = request.DATA , files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageDetail(generics.RetrieveAPIView):
    model = Image
    serializer_class = ImageSerializer       

''' views for comments'''
class CommentList(generics.ListAPIView):
    model = Comment
    serializer_class = CommentSerializer
    filter_fields=('name', 'created')
    def get(self, request):
        kiosk_id = self.request.QUERY_PARAMS.get('kiosk', None)
        return getSetForKioskId(Comment, CommentSerializer, kiosk_id)
    
    def post(self, request):
        serializer = CommentSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(generics.CreateAPIView):
    model = Comment
    serializer_class = CommentSerializer 
    
  
''' views for beers'''
class BeerPriceList(generics.ListCreateAPIView):
    model = BeerPrice
    serializer_class = BeerPriceSerializer
    def get(self, request):
        kiosk_id = self.request.QUERY_PARAMS.get('kiosk', None)
        return getSetForKioskId(BeerPrice, BeerPriceSerializer, kiosk_id)


class BeerPriceDetail(generics.RetrieveUpdateAPIView):
    model=BeerPrice
    serializer_class = BeerPriceSerializer


class BeerList(generics.ListAPIView):
    model = Beer
    serializer_class = BeerSerializer
    filter_fields=['name', 'brand', 'location', 'brew']
    def get(self, request):
        kiosk_id = self.request.QUERY_PARAMS.get('kiosk', None)
        if kiosk_id is not None:
            if not check_kiosk_args(kiosk_id):
                return HttpResponseBadRequest("Kiosk id arguments was malformed")
            beerSet = Beer.objects.filter(related_beer__kiosk__id = kiosk_id)
            if beerSet.count()== 0:
                return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            beerSet = Beer.objects.all()
             
        serializer = BeerSerializer(beerSet, many=True)
        return Response(serializer.data)
    
    
class BeerDetail(generics.RetrieveAPIView):
    model=Beer
    serializer_class = BeerSerializer
    

''' views for kiosk'''
class SimpleKioskList(generics.ListCreateAPIView):
    model = Kiosk
    serializer_class = KioskSerializer
    filter_fields = ('id', 'name', 'owner', 'street','city','zip_code')
    def post(self, request):
        serializer = KioskSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
          
        log.warn("Serializer is invalid for kiosk put. : " + str(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     

class KioskDetail(APIView):
    def get_object(self, kiosk_id):
        try:
            return Kiosk.objects.get(pk=kiosk_id)
        except Kiosk.DoesNotExist:
            raise Http404

    def get(self, request, kiosk_id):
        k = self.get_object(kiosk_id)
        serializer = KioskSerializer(k)
        return Response(serializer.data)
    

''' An object to hold all the info the kiosk detail view on the client needs. this will be passed to the serializer'''
class KioskDetailContainer(object):
    def __init__(self, kiosk, beerPrice=None, images=None, comments = None):
        self.kiosk = kiosk
        self.beerPrice = beerPrice
        self.images = images
        self.comments = comments
        
        
''' this will get the kiosk with the given id from the database and pulls all the necessary info from the connected tables''' 
class KioskDetailView(APIView):
    
    def get_object(self, primaryKey):
        try:
            return Kiosk.objects.get(pk=primaryKey)
        except Kiosk.DoesNotExist:
            raise Http404

    def get(self, request, primaryKey):
        kiosk = self.get_object(primaryKey)
        imageSet = Image.objects.filter(kiosk__pk = kiosk.id)
        commentSet = Comment.objects.filter(kiosk__pk = kiosk.id)
        beerPriceSet = BeerPrice.objects.filter(kiosk__id = kiosk.id).order_by('score')
        l = KioskDetailContainer(kiosk, beerPrice=beerPriceSet, images=imageSet, comments=commentSet)
        serializer = KioskDetailSerializer(l)
        return Response(serializer.data)
    

'''angle to radians conversion'''
def radians(r):
    return r * math.pi / 180
''' simple pythagorean distance for flat surfaces. Returns distance in kilometers!'''
def calculate_distance(lat_1,lon_1  ,  lat_2,lon_2):
    R = 6371
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)
    lon_1 = radians(lon_1)
    lon_2 = radians(lon_2)
    x = (lon_2-lon_1) * math.cos((lat_1+lat_2)/2);
    y = (lat_2-lat_1);
    return math.sqrt(x*x + y*y) * R;



''' An Object to hold all the stuff needed for a listItem. This Object will be provided to the Serializer'''
class ListItem(object):
    def __init__(self, kiosk, beerPrice=None, thumb=None, distance = 0):
        self.kiosk = kiosk
        self.beerPrice = beerPrice
        self.thumb = thumb
        self.distance = distance
        
        
'''
    returns a listitem object  given a specific kiosk and the lat,long values of the client
    so it can calculate the distance between kiosk and client to write into the listitem object
    if a beer argument is supplied only kioskItems containg that beer will be returned
'''
def getListItemFromKiosk(kiosk, lat = None, lon = None, beer=None):
    img = None
    beerPrice = None
    imageSet = Image.objects.filter(kiosk__pk = kiosk.id)
    if imageSet.exists():
        img = imageSet[0].image['thumbnail'].url

    beerPriceSet = BeerPrice.objects.filter(kiosk__id = kiosk.id).order_by('score')
    if beerPriceSet.exists():
        if beer is not None:
            beerPriceSet = beerPriceSet.filter(beer__name__icontains = beer)
            if not beerPriceSet.exists():
                return None
        beerPrice = beerPriceSet[0]
    else:
        if beer is not None:
            return None
    if lat is not None and lon is not None:
        distance = calculate_distance(float(kiosk.geo_lat), float(kiosk.geo_long), lat, lon)
        return ListItem(kiosk=kiosk, thumb=img, beerPrice = beerPrice, distance = distance )

    return ListItem(kiosk=kiosk, thumb=img, beerPrice = beerPrice )
    

''' 
    View to return a list of kioskItems where the kiosk is within a boundingbox with the length radius supplied in the url
    in case the parameter contain bullshit values this will raise a ERROR400 bad request to the client
''' 
class KioskList(APIView):

    def get(self, request):
        #get parameters from httprequest
        #in case url contains bullshit for lat,long or radius this will throw a value exception
        #default values 5km radius 
        g_lat = 51.52
        g_long = 7.46
        radius = 5.0
        beer = None
        #check url parameter 
        try:
            if request.QUERY_PARAMS.get('geo_lat', None) is not None:
                g_lat = float(request.QUERY_PARAMS.get('geo_lat', None))
            if request.QUERY_PARAMS.get('geo_long', None) is not None:
                g_long = float(request.QUERY_PARAMS.get('geo_long', None))
            if request.QUERY_PARAMS.get('radius', None) is not None:
                radius = float(request.QUERY_PARAMS.get('radius', None))
            if request.QUERY_PARAMS.get('beer', None) is not None:
                beer = request.QUERY_PARAMS.get('beer', None)
        except :
            return HttpResponseBadRequest('bad parameter string')

        max_distance = radius;
        #radius from km to degrees
        R = 6371 # earth radius
        #from a length to radians. see definition of a radian
        radius = radius/R
        # now convert radians to degrees
        radius = radius*180/math.pi
        
        #get all kiosk within the bounding box
        queryResult = Kiosk.objects.filter(geo_lat__lte = g_lat + radius, geo_long__lte = g_long + radius, geo_lat__gte = g_lat - radius, geo_long__gte = g_long - radius)
  
        #build a kiosklistem for every kiosk we fetched and return it through the serializer
        l = list()
        for kiosk in queryResult:
            item = getListItemFromKiosk(kiosk, g_lat, g_long, beer)
            if item is not None and item.distance <= max_distance :
                l.append(item)
        
        serializer = KioskListItemSerializer(l, many=True)
        return Response(serializer.data)
        

''' View for a single kiosklistitem does not take any parameter'''
class KioskListItem(APIView):
    
    def get_object(self, primaryKey):
        try:
            return Kiosk.objects.get(pk=primaryKey)
        except Kiosk.DoesNotExist:
            raise Http404

    def get(self, request, primaryKey):
        kiosk = self.get_object(primaryKey)
        l = getListItemFromKiosk(kiosk)
        serializer = KioskListItemSerializer(l)
        return Response(serializer.data)
    
