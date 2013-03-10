from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from bier import views

urlpatterns = patterns('',
    url(r'^rest/beer/$', views.BeerList.as_view()),
    url(r'^rest/beer/(?P<beer_id>[0-9]+)$', views.BeerDetail.as_view()),

    url(r'^rest/kiosk/$', views.KioskList.as_view()),
    url(r'^rest/kiosk/(?P<kiosk_id>[0-9]+)/$', views.KioskDetail.as_view() ),
    
    url(r'^rest/image/$', views.ImageList.as_view() ),
    url(r'^rest/image/(?P<kiosk_id>[0-9]+)/$', views.ImageDetail.as_view() ),
    
    url(r'^(?P<kiosk_id>[0-9]+)/$', 'bier.views.biere'),
    url(r'^$', 'bier.views.kiosk', name='kiosk'),
    
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': '/home/bier/html/static'})

)

urlpatterns = format_suffix_patterns(urlpatterns)
