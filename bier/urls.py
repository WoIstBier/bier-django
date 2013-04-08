# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from bier import views

urlpatterns = patterns('',
    url(r'^rest/beer/$', views.BeerList.as_view()),
    url(r'^rest/beer/(?P<pk>[0-9]+)$', views.BeerDetail.as_view()),

    url(r'^rest/beerprice/$', views.BeerPriceList.as_view() ),
    url(r'^rest/beerprice/(?P<pk>[0-9]+)$', views.BeerPriceDetail.as_view()),
    
    url(r'^rest/kiosk/$', views.KioskList.as_view()),
    url(r'^rest/kiosk/(?P<kiosk_id>[0-9]+)/$', views.KioskDetail.as_view() ),
    
    url(r'^rest/image/$', views.ImageList.as_view() ),
    url(r'^rest/image/(?P<pk>[0-9]+)/$', views.ImageDetail.as_view() ),
    
    url(r'^rest/comment/$', views.CommentList.as_view() ),
    url(r'^rest/comment/(?P<pk>[0-9]+)/$', views.CommentDetail.as_view() ),
    
    
    url(r'^web/(?P<kiosk_id>[0-9]+)/$', 'bier.views.biere'),
    url(r'^web/$', 'bier.views.kiosk', name='kiosk'),

)

urlpatterns = format_suffix_patterns(urlpatterns)
