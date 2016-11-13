# -*- coding: utf-8 -*-
# Create your views here.
from woistbier_rest.models import Kiosk, BeerPrice, Image, Beer, Comment
from woistbier_rest.serializers import KioskSerializer, ImageSerializer, BeerSerializer, CommentSerializer, BeerPriceSerializer, KioskListItemSerializer, KioskDetailSerializer
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render_to_response
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from django.db.models import Avg
import math
import logging

import django_filters
log = logging.getLogger(__name__)


def not_found_view(request):
    response = render_to_response('bier/404.html')
    response.status_code = 404
    return response


def index(request):
    num_kiosk = Kiosk.objects.all().count()
    num_beer = Beer.objects.all().count()
    return render_to_response('bier/index.html', {'kiosk_number': num_kiosk, 'beer_number': num_beer})


def beer_list(request):
    num_beer = Beer.objects.all().count()
    return render_to_response('bier/beer.html', {'beer_count': num_beer})


def impressum(request):
    return render_to_response('bier/impressum.html')


#Here come the views for the rest api


def check_kiosk_args(kiosk_id):
    if kiosk_id is None:
        return False
    try:
        int(kiosk_id)
    except ValueError:
        return False
    return True


def check_if_kiosk_exists(kiosk_id):
    try:
        Kiosk.objects.get(pk = kiosk_id)
    except Kiosk.DoesNotExist:
        return False
    return True


#views for images
class ImageList(generics.ListAPIView):
    serializer_class = ImageSerializer
    filter_fields = ['kiosk']
    queryset = Image.objects.all()

    def post(self, request):
        #curl -X POST -S -H 'Accept: application/json' -F "image=@/home/mackaiver/Pictures/alf2.jpg; type=image/jpg"
        #                           http://localhost:8000/bier/rest/image/68/
        # print(str(request))
        serializer = ImageSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetail(generics.RetrieveAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    filter_fields = ('name', 'created', 'kiosk')
    queryset = Comment.objects.all()

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(generics.RetrieveUpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class BeerPriceList(generics.ListCreateAPIView):
    queryset = BeerPrice.objects.all()
    serializer_class = BeerPriceSerializer
    filter_fields = ['kiosk', 'beer']


class BeerPriceDetail(generics.RetrieveUpdateAPIView):
    queryset = BeerPrice.objects.all()
    serializer_class = BeerPriceSerializer



class BeerListFilter(django_filters.FilterSet):
    kiosk = django_filters.NumberFilter(name="related_beer__kiosk__id")

    class Meta:
        model = Beer
        fields = ['name', 'brand', 'location', 'brew']

class BeerList(generics.ListAPIView):
    serializer_class = BeerSerializer
    queryset = Beer.objects.all()
    filter_class = BeerListFilter


class BeerDetail(generics.RetrieveUpdateAPIView):
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer


class SimpleKioskList(generics.ListCreateAPIView):
    queryset = Kiosk.objects.all()
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'kiosk_uploads'
    model = Kiosk
    serializer_class = KioskSerializer
    filter_fields = ('id', 'name', 'owner', 'street', 'city', 'zip_code')

    def post(self, request, *args, **kwargs):
        serializer = KioskSerializer(data=request.data)
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


#An object to hold all the info the kiosk detail view on the client needs. this will be passed to the serializer
class KioskDetailContainer(object):
    def __init__(self, kiosk, beerPrice=None, images=None, comments = None, comment_count = 0, beer_count = 0, avg_price = 1):
        self.kiosk = kiosk
        self.beerPrice = beerPrice
        self.images = images
        self.comments = comments
        self.comment_count = comment_count
        self.beer_count = beer_count
        self.avg_price = avg_price


# this will get the kiosk with the given id from the database and pulls all the necessary info from the connected tables
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
        beer_count = beerPriceSet.count()
        comment_count = commentSet.count()
        avg_price = beerPriceSet.aggregate(Avg('score'))
        l = KioskDetailContainer(kiosk, beerPrice=beerPriceSet, images=imageSet, comments=commentSet,
                                 comment_count=comment_count, beer_count=beer_count, avg_price=avg_price)
        serializer = KioskDetailSerializer(l)
        return Response(serializer.data)


#angle to radians conversion
def radians(r):
    return r * math.pi / 180


# simple pythagorean distance for flat surfaces. Returns distance in kilometers!
def calculate_distance(lat_1, lon_1, lat_2, lon_2):
    R = 6371
    lat_1 = radians(lat_1)
    lat_2 = radians(lat_2)
    lon_1 = radians(lon_1)
    lon_2 = radians(lon_2)
    x = (lon_2-lon_1) * math.cos((lat_1+lat_2)/2)
    y = (lat_2-lat_1)
    return math.sqrt(x*x + y*y) * R


#An Object to hold all the stuff needed for a listItem. This Object will be provided to the Serializer
class ListItem(object):
    def __init__(self, kiosk, beer_price=None, image=None, distance=0.0):
        self.kiosk = kiosk
        self.beerPrice = beer_price
        self.image = image
        self.distance = distance


#
#   returns a listitem object  given a specific kiosk and the lat,long values of the client
#   so it can calculate the distance between kiosk and client to write into the listitem object
#   if a beer argument is supplied only kioskItems containg that beer will be returned
#
def get_list_item_from_kiosk(kiosk, lat=None, lon=None, beer=None):
    img = None
    beerPrice = None
    imageSet = Image.objects.filter(kiosk__pk=kiosk.id)
    if imageSet.exists():
        img = imageSet[0]

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
        return ListItem(kiosk=kiosk, beer_price=beerPrice,  image=img, distance=distance)

    return ListItem(kiosk=kiosk, beer_price=beerPrice, thumb=img)


#View to return a list of kioskItems where the kiosk is within a boundingbox with the length radius supplied in the url
#in case the parameter contain bullshit values this will raise a ERROR400 bad request to the client
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
            if request.query_params.get('geo_lat', None) is not None:
                g_lat = float(request.query_params.get('geo_lat', None))
            if request.query_params.get('geo_long', None) is not None:
                g_long = float(request.query_params.get('geo_long', None))
            if request.query_params.get('radius', None) is not None:
                radius = float(request.query_params.get('radius', None))
            if request.query_params.get('beer', None) is not None:
                beer = request.query_params.get('beer', None)
        except :
            return HttpResponseBadRequest('bad parameter string')

        max_distance = radius;
        #radius from km to degrees
        R = 6371  # earth radius
        #from a length to radians. see definition of a radian
        radius = radius/R
        # now convert radians to degrees
        radius = radius*180/math.pi

        #get all kiosk within the bounding box
        queryResult = Kiosk.objects.filter(geo_lat__lte = g_lat + radius, geo_long__lte = g_long + radius, geo_lat__gte = g_lat - radius, geo_long__gte = g_long - radius)

        #build a kiosklistem for every kiosk we fetched and return it through the serializer
        l = list()
        for kiosk in queryResult:
            item = get_list_item_from_kiosk(kiosk, g_lat, g_long, beer)
            if item is not None and item.distance <= max_distance :
                l.append(item)

        serializer = KioskListItemSerializer(l, many=True)
        return Response(serializer.data)


# View for a single kiosklistitem does not take any parameter
class KioskListItem(APIView):

    def get_object(self, primaryKey):
        try:
            return Kiosk.objects.get(pk=primaryKey)
        except Kiosk.DoesNotExist:
            raise Http404

    def get(self, request, primaryKey):
        kiosk = self.get_object(primaryKey)
        l = get_list_item_from_kiosk(kiosk)
        serializer = KioskListItemSerializer(l)
        return Response(serializer.data)
