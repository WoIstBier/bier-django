from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from bier import views

urlpatterns = patterns('',
    url(r'^rest/$', views.KioskList.as_view()),
    url(r'^(?P<kiosk_id>[0-9]+)/$', 'bier.views.biere'),
    url(r'^$', 'bier.views.index', name='index'),

)

urlpatterns = format_suffix_patterns(urlpatterns)
