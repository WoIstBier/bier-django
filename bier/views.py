# Create your views here.
from bier.models import Kiosk, BeerPrice, KioskImage, ImageForm, Image, Beer
from bier.serializers import KioskSerializer, ImageSerializer, BeerSerializer
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError




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

class ImageList(generics.ListAPIView):
    model = Image
    serializer_class = ImageSerializer
    
class ImageDetail(APIView):
    model = Image
    serializer_class = ImageSerializer
#    filter_fields=('id', 'image.name')
    def get(self, request, kiosk_id):
        kiosk = Kiosk.objects.get(pk = kiosk_id)
        kImgSet = KioskImage.objects.filter(kiosk = kiosk)
        imgSet = Image.objects.filter(pk__in =  kImgSet.values_list('img'))
        serializer = ImageSerializer(imgSet, many=True)
        return Response(serializer.data)
        
        
        
    def post(self, request, kiosk_id):
        serializer = ImageSerializer(data = request.DATA , files=request.FILES, context={'kiosk_id': kiosk_id, 'request' : request})
#        print('request data:  ' + str(request.DATA['image']) + '\n')
        print('files: ' + str(request.FILES['image']) + '\n')
        if serializer.is_valid():
            serializer.save()
            imageId = serializer.object.id
            k = KioskImage(kiosk = Kiosk.objects.get(pk=kiosk_id) , img=Image.objects.get(pk = imageId))
            k.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BeerList(generics.ListAPIView):
    model = Beer
    serializer_class = BeerSerializer
    filter_fields=('name', 'brand', 'location')

class BeerDetail(APIView):
    def get_object(self, beer_id):
        try:
            return Beer.objects.get(pk=beer_id)
        except Beer.DoesNotExist:
            raise Http404
        
    def get(self, request, beer_id):
        k = self.get_object(beer_id)
        serializer = BeerSerializer(k)
        return Response(serializer.data)

class KioskList(generics.ListAPIView):
    model = Kiosk
    serializer_class = KioskSerializer
    filter_fields = ('id', 'name', 'owner', 'street')
    
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
