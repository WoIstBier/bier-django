# Create your views here.
from polls.models import Kiosk, BierPreisListe
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    kiosk_liste = Kiosk.objects.order_by('name')
    context = {'kioske': kiosk_liste}
    return render(request, 'polls/index.html', context)

def preise(request):
    bier_liste = BierPreisListe.objects.order_by('preis')
    context = {'bier_liste': bier_liste}
    return render(request, 'polls/bier.html', context)

#def index(request):
#    return HttpResponse("Hello, world. You're at the poll index.")