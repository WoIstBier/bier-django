from django.conf.urls import patterns, url

from bier import views

urlpatterns = patterns('',
    url(r'^polls/(?P<kiosk_id>\d+)/$', 'polls.views.biere'),
    url(r'^$', views.index, name='index'),
)