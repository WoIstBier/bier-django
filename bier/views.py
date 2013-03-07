# Create your views here.
from bier.models import Kiosk, BeerPrice, KioskImage, ImageForm, Image
from bier.serializers import KioskSerializer
from django.template import RequestContext

from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from rest_framework.views import APIView
from rest_framework.response import Response

def index(request):
    kiosk_liste = Kiosk.objects.order_by('name')
    return render_to_response('bier/index.html', {'kioske': kiosk_liste })

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
            return HttpResponseRedirect(reverse('bier.views.index'))
        else:
            print('form is invalid')
    else:
        form = ImageForm()
        
#    inner_qs = Blog.objects.filter(name__contains='Cheddar')
#    entries = Entry.objects.filter(blog__in=inner_qs)

#    r = Rating.objects.get( id=rating_id )
#    c = r.candidate_set().all()
    p = BeerPrice.objects.filter(id = kiosk_id)
    k = KioskImage.objects.filter(kiosk__pk = kiosk_id)
    imgSet = Image.objects.filter(pk__in =  k.values_list('img'))
    c = RequestContext(request,  {'bier_list': p, 'form' : form, 'imgs': imgSet, 'kiosk': Kiosk.objects.get(pk=kiosk_id) })
    return render_to_response('bier/biere.html', c)

def detail(request, poll_id):
    return HttpResponse("You're looking at poll %s." % poll_id)
#def index(request):
#    return HttpResponse("Hello, world. You're at the poll index.")


class KioskList(APIView):
    def get(self, request, format=None):
        ks = Kiosk.objects.all()
        serializer = KioskSerializer(ks, many=True)
        return Response(serializer.data)

#    def post(self, request, format=None):
#        serializer = KioskSerializer(data=request.DATA)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class KioskDetail(APIView):
    def get_object(self, pk):
        try:
            return Kiosk.objects.get(pk=pk)
        except Kiosk.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        k = self.get_object(pk)
        serializer = KioskSerializer(k)
        return Response(serializer.data)