# Create your views here.
from polls.models import Kiosk
from django.shortcuts import render


def index(request):
    kiosk_liste = Kiosk.objects.order_by(Kiosk.name)
    context = {'kioske': kiosk_liste}
    return render(request, 'polls/index.html', context)

