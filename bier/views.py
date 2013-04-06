# -*- coding: utf-8 -*-
# Create your views here.
from bier.models import Kiosk, BeerPrice, KioskImage, ImageForm, Image, Beer, Comment, KioskComments
from bier.serializers import KioskSerializer, ImageSerializer, BeerSerializer, CommentSerializer, BeerPriceSerializer
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
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
            k = KioskImage(kiosk = Kiosk.objects.get(pk=kiosk_id) , img=imgModel)
            k.save()
            return HttpResponseRedirect(reverse('bier.views.kiosk'))
        else:
            print('form is invalid')
    else:
        form = ImageForm()
        
    p = BeerPrice.objects.filter(id = kiosk_id)
    k = KioskImage.objects.filter(kiosk__pk = kiosk_id)
    imgSet = Image.objects.filter(pk__in =  k.values_list('img'))
    c = RequestContext(request,  {'bier_list': p, 'form' : form, 'imgs': imgSet, 'kiosk': Kiosk.objects.get(pk=kiosk_id) })
    return render_to_response('bier/biere.html', c)




'''
Here come the views for the rest api
'''

''' Some helper Functions'''
def check_kiosk_args(self, kiosk_id):
    try:
        long(kiosk_id)
    except ValueError:
        raise HttpResponseBadRequest
    try:
        Kiosk.objects.get(pk = kiosk_id)
    except Kiosk.DoesNotExist:
        raise Http404
    

def getObjectsForKioskId(self, relationClass,resultClass,  attributeName, kiosk_id):
    check_kiosk_args(self, kiosk_id)
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
            imgSet = getObjectsForKioskId(self, KioskImage, Image,  'img', kiosk_id)
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
        check_kiosk_args(self, kiosk_id)
        serializer = ImageSerializer(data = request.DATA , files=request.FILES, context={'kiosk_id': kiosk_id, 'request' : request})
        if serializer.is_valid():
            serializer.save()
            imageId = serializer.object.id
            k = KioskImage(kiosk = Kiosk.objects.get(pk=kiosk_id) , img=Image.objects.get(pk = imageId))
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
            commentSet = getObjectsForKioskId(self, KioskComments, Comment, 'comment', kiosk_id)
            if commentSet.count()== 0:
                return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            commentSet = Comment.objects.all()
            
        serializer = CommentSerializer(commentSet, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        kiosk_id = self.request.QUERY_PARAMS.get('kiosk', None)
        check_kiosk_args(self, kiosk_id);
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
            check_kiosk_args(self, kiosk_id)
            beer_price_set = BeerPrice.objects.filter(kiosk__id = kiosk_id)
            if beer_price_set.count()== 0:
                return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            beer_price_set = BeerPrice.objects.all()
             
        serializer = BeerPriceSerializer(beer_price_set, many=True)
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
class KioskList(generics.ListAPIView):
    model = Kiosk
    serializer_class = KioskSerializer
    filter_fields = ('id', 'name', 'owner', 'street','city','zip_code')
#    TODO: data checks. prevent duplicates
    def post(self, request):
        serializer = KioskSerializer(data=request.DATA)
        if serializer.is_valid():
            k = serializer.save()
            if k.doubleEntry or not k.is_valid_address:
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
          
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        log.error("Serializer is invalid for kiosk put. : " + str(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        """
        Filter Kiosks by beer that is being sold there
        """
        legal_arguments = ('id', 'name', 'owner', 'street') + ('beer_name', 'beer_brand', 'brand_location')
        
        for param in self.request.QUERY_PARAMS:
            if param not in legal_arguments:
                #bad request
                raise ParseError(detail=None)
            
        beerName = self.request.QUERY_PARAMS.get('beer_name', None)
        beerBrand = self.request.QUERY_PARAMS.get('beer_brand', None)
        beerLocation = self.request.QUERY_PARAMS.get('brand_location', None)
        if beerName is None and beerBrand is None and beerLocation is None:
            ks = Kiosk.objects.all()
            return ks
        p = BeerPrice.objects.none()
        if beerName:
            p = BeerPrice.objects.filter(beer__name = beerName )
        if beerBrand:
            p2 =  BeerPrice.objects.filter(beer__brand = beerBrand )
            if p.exists():
                p = p & p2
            else:
                p = p2 
        if beerLocation:
            pLoc = BeerPrice.objects.filter(beer__location = beerLocation )
            if p:
                p = p & pLoc
            else:
                p = pLoc

        ks = Kiosk.objects.filter(pk__in = p.values_list('kiosk'))
        return ks
    

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
