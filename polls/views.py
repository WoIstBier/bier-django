# Create your views here.
from polls.models import BierPreisListe
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from polls.models import Kiosk
from polls.serializers import KioskSerializer

def index(request):
    kiosk_liste = Kiosk.objects.order_by('name')
    context = {'kioske': kiosk_liste}
    return render(request, 'polls/index.html', context)

def biere(request, kiosk_id):
    p = BierPreisListe.objects.filter('id' == kiosk_id)
    return render_to_response('polls/biere.html', {'biere': p})

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