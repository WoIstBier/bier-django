from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from bier import views

urlpatterns = patterns('',
    url(r'^polls/$', views.KioskList.as_view()),
    url(r'^polls/(?P<pk>[0-9]+)/$', views.KioskDetail.as_view()),
#    url(r'^polls/(?P<kiosk_id>[0-9]+)/$', 'polls.views.biere'),
#    url(r'^$', views.index, name='index'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
