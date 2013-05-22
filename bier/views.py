# -*- coding: utf-8 -*-
# Create your views here.
from bier.models import Kiosk, BeerPrice, KioskImage, ImageForm, Image, Beer, Comment, KioskComments
from bier.serializers import KioskSerializer, ImageSerializer, BeerSerializer, CommentSerializer, BeerPriceSerializer, KioskListItemSerializer, KioskDetailSerializer
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
import math
import logging
log = logging.getLogger(__name__)



def index(request):
    return render_to_response('bier/index.html')

def kiosk(request):
    kiosk_liste = Kiosk.objects.order_by('name')
    return render_to_response('bier/kiosk.html', {'kioske': kiosk_liste })

def biere(request, kiosk_id):
    print('in bier view')
    if request.method =='POST':
        print('Post request')
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            print('form is valid')
            imgModel = Image(image=request.FILES['image'], thumbnail=None)
            imgModel.save()
            k = KioskImage(kiosk = Kiosk.objects.get(pk=kiosk_id) , image=imgModel)
            k.save()
            return HttpResponseRedirect(reverse('bier.views.kiosk'))
        else:
            print('form is invalid')
    else:
        form = ImageForm()
        
    p = BeerPrice.objects.filter(id = kiosk_id)
    k = KioskImage.objects.filter(kiosk__pk = kiosk_id)
    imgSet = Image.objects.filter(pk__in =  k.values_list('image'))
    c = RequestContext(request,  {'bier_list': p, 'form' : form, 'imgs': imgSet, 'kiosk': Kiosk.objects.get(pk=kiosk_id) })
    return render_to_response('bier/biere.html', c)




'''
Here come the views for the rest api
'''

''' Some helper Functions'''
def check_kiosk_args(kiosk_id):
    if kiosk_id == None:
        raise HttpResponseBadRequest
    try:
        long(kiosk_id)
    except ValueError:
        raise HttpResponseBadRequest
    try:
        Kiosk.objects.get(pk = kiosk_id)
    except Kiosk.DoesNotExist:
        raise Http404
    

def getObjectsForKioskId(relationClass,resultClass,  attributeName, kiosk_id):
    check_kiosk_args(kiosk_id)
    relationSet = relationClass.objects.filter(kiosk__id = kiosk_id)
    return resultClass.objects.filter(pk__in =  relationSet.values_list(attributeName))
    
''' views for images'''
class ImageList(APIView):
        
    def get(self, request, format = None):
        kiosk_id = self.request.QUERY_PARAMS.get('kiosk', None)
        if kiosk_id is not None:
#             check_kiosk_args(kiosk_id)
#             kImgSet = KioskImage.objects.filter(kiosk__id = kiosk_id)
#             imgSet = Image.objects.filter(pk__in =  kImgSet.values_list('img'))
            imgSet = getObjectsForKioskId(KioskImage, Image,  'image', kiosk_id)
            if imgSet.count()== 0:
                return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            imgSet = Image.objects.all()
            
        serializer = ImageSerializer(imgSet, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        #curl -X POST -S -H 'Accept: application/json' -F "image=@/home/mackaiver/Pictures/alf2.jpg; type=image/jpg" http://localhost:8000/bier/rest/image/68/
        kiosk_id = self.request.QUERY_PARAMS.get('kiosk', None)
        if kiosk_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        #self.check_kiosk_args(kiosk_id)
        check_kiosk_args(kiosk_id)
        serializer = ImageSerializer(data = request.DATA , files=request.FILES, context={'kiosk_id': kiosk_id, 'request' : request})
        if serializer.is_valid():
            serializer.save()
            imageId = serializer.object.id
            k = KioskImage(kiosk = Kiosk.objects.get(pk=kiosk_id) , image=Image.objects.get(pk = imageId))
            k.save()
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
    def get(self, request, format = None):
        kiosk_id = self.request.QUERY_PARAMS.get('kiosk', None)
        if kiosk_id is not None:
            commentSet = getObjectsForKioskId( KioskComments, Comment, 'comment', kiosk_id)
            if commentSet.count()== 0:
                return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            commentSet = Comment.objects.all()
            
        serializer = CommentSerializer(commentSet.order_by('-created'), many=True)
        return Response(serializer.data)
    
    def post(self, request):
        kiosk_id = self.request.QUERY_PARAMS.get('kiosk', None)
        check_kiosk_args(kiosk_id);
        serializer = CommentSerializer(data=request.DATA)
        if serializer.is_valid():
            com = serializer.save()
            k = KioskComments(kiosk = Kiosk.objects.get(pk=kiosk_id) , comment = com)
            k.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(generics.CreateAPIView):
    model = Comment
    serializer_class = CommentSerializer 
    
  
''' views for beers'''
class BeerPriceList(generics.ListCreateAPIView):
    model = BeerPrice
    serializer_class = BeerPriceSerializer
    def get(self, request, format = None):
        kiosk_id = self.request.QUERY_PARAMS.get('kiosk', None)
        if kiosk_id is not None:
            check_kiosk_args(kiosk_id)
            beer_price_set = BeerPrice.objects.filter(kiosk__id = kiosk_id)
            if beer_price_set.count()== 0:
                return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            beer_price_set = BeerPrice.objects.all()
             
        serializer = BeerPriceSerializer(beer_price_set.order_by('beer__name'), many=True)
        return Response(serializer.data)


class BeerPriceDetail(generics.RetrieveUpdateAPIView):
    model=BeerPrice
    serializer_class = BeerPriceSerializer


class BeerList(generics.ListAPIView):
    model = Beer
    serializer_class = BeerSerializer
    filter_fields=['name', 'brand', 'location', 'brew']
    def get(self, request, format = None):
        kiosk_id = self.request.QUERY_PARAMS.get('kiosk', None)
        if kiosk_id is not None:
            beerSet = getObjectsForKioskId(self, BeerPrice, Beer, 'beer', kiosk_id)
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
#    TODO: data checks. prevent duplicates
    def post(self, request):
        serializer = KioskSerializer(data=request.DATA)
        if serializer.is_valid():
            k = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
         
        log.error("Serializer is invalid for kiosk put. : " + str(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class KioskDetail(APIView):
    def get_object(self, kiosk_id):
        try:
            return Kiosk.objects.get(pk=kiosk_id)
        except Kiosk.DoesNotExist:
            raise Http404

    def get(self, request, kiosk_id, format=None):
        k = self.get_object(kiosk_id)
        serializer = KioskSerializer(k)
        return Response(serializer.data)
    
#     def put(self, request,kiosk_id, format=None):
#         serializer = KioskSerializer(data=request.DATA)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        imageSet = getObjectsForKioskId(KioskImage, Image, 'image',  kiosk.id)
        commentSet = getObjectsForKioskId(KioskComments, Comment, 'comment',  kiosk.id)
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
'''
def getListItemFromKiosk(kiosk, lat = None, lon = None, beer=None):
    img = None
    beerPrice = None
    imageSet = getObjectsForKioskId(KioskImage, Image, 'image',  kiosk.id)
    if imageSet.exists():
        img = imageSet[0]

    beerPriceSet = BeerPrice.objects.filter(kiosk__id = kiosk.id).order_by('score')
    if beerPriceSet.exists():
        if beer is not None:
            beerPriceSet = beerPriceSet.filter(beer__name__icontains = beer)
            if not beerPriceSet.exists():
                return None
        beerPrice = beerPriceSet[0]
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
            if item is not None:
                l.append(item)
        
        #sort the list by the key returned by the lambda function. distance is the default
#         legalSortKeys=['price', 'distance', 'street', 'beer']
#         if not sort in legalSortKeys:
#             sort = "distance"
#         if sort == "distance":
#             l.sort(key=lambda item: item.distance  , reverse=False)
#         elif sort == "price":
#             l.sort(key=lambda item: item.beerPrice.score  , reverse=False)
#         elif sort == "street":
#             l.sort(key=lambda item: item.kiosk.street  , reverse=False)
#         elif sort == "beer":
#             l.sort(key=lambda item: item.beerPrice.beer.name  , reverse=False)
        
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
    
