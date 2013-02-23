# Create your views here.
from polls.models import Kiosk, BierPreisListe
from django.shortcuts import render_to_response, get_object_or_404, render
from django.http import HttpResponse


def index(request):
    kiosk_liste = Kiosk.objects.order_by('name')
    context = {'kioske': kiosk_liste}
    return render(request, 'bier/index.html', context)

def biere(request, kiosk_id):
    p = BierPreisListe.objects.filter('id' == kiosk_id)
    return render_to_response('polls/biere.html', {'biere': p})

def detail(request, poll_id):
    return HttpResponse("You're looking at poll %s." % poll_id)
#def index(request):
#    return HttpResponse("Hello, world. You're at the poll index.")