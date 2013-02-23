'''
Created on Feb 17, 2013

@author: mackaiver
'''
from django.conf.urls import patterns, url

from bier import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)