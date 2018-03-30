# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from woistbier_rest import views

urlpatterns = [
    url(r'^$', views.api_index),
    url(r'^rest/beer/?$', views.BeerList.as_view()),
    url(r'^rest/beer/(?P<pk>[0-9]+)/?$', views.BeerDetail.as_view()),

    url(r'^rest/beerprice/?$', views.BeerPriceList.as_view() ),
    url(r'^rest/beerprice/(?P<pk>[0-9]+)/?$', views.BeerPriceDetail.as_view()),

    url(r'^rest/kiosk/?$', views.SimpleKioskList.as_view()),
    url(r'^rest/kiosk/(?P<kiosk_id>[0-9]+)/?$', views.KioskDetail.as_view() ),

    url(r'^rest/image/?$', views.ImageList.as_view() ),
    url(r'^rest/image/(?P<pk>[0-9]+)/?$', views.ImageDetail.as_view() ),

    url(r'^rest/comment/?$', views.CommentList.as_view() ),
    url(r'^rest/comment/(?P<pk>[0-9]+)/?$', views.CommentDetail.as_view() ),

    url(r'^rest/kioskList/?$', views.KioskList.as_view()),
    url(r'^rest/kioskList/(?P<primaryKey>[0-9]+)/?$', views.KioskListItem.as_view()),
    
    url(r'^rest/kioskDetails/(?P<primaryKey>[0-9]+)/?$', views.KioskDetailView.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
