from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from bier import views

urlpatterns = patterns('',
    url(r'^rest/$', views.KioskList.as_view()),
    url(r'^rest/bier=(?P<beerName>(\w)+)$', views.KioskList.as_view()),
    url(r'^rest/(?P<kiosk_id>[0-9]+)/$', views.KioskDetail.as_view() ),
    url(r'^rest/kioskimages/(?P<kiosk_id>[0-9]+)/$', views.ImageList.as_view() ),
    url(r'^(?P<kiosk_id>[0-9]+)/$', 'bier.views.biere'),
    url(r'^$', 'bier.views.kiosk', name='kiosk'),

)

urlpatterns = format_suffix_patterns(urlpatterns)
