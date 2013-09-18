from django.conf.urls import patterns, include, url
from settings import MEDIA_ROOT, STATIC_ROOT
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import logging
log = logging.getLogger(__name__)
import socket
print(str(socket.gethostname()))
if  socket.gethostname().startswith('Novalee'):
    LOCALHOST = True
else: 
    LOCALHOST = False

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'siteStuff.views.home', name='home'),
    # url(r'^siteStuff/', include('siteStuff.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #include the urls from the polls app.
    url(r'^bier/', include('bier.urls')),
    
#     url(r'^$', TemplateView.as_view(template_name="index.html")),
    
    url(r'^$', 'bier.views.index',name="index"),
    url(r'^about', 
        TemplateView.as_view(template_name='bier/contact.html'),
        name='about'),
    url(r'^testPage', 
        TemplateView.as_view(template_name='bier/testPage/index.html'),
        name='test_about')
                       
)

handler404 = 'bier.views.not_found_view'

if LOCALHOST:
    append= patterns( '',  
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$','django.views.static.serve',{
            'document_root': STATIC_ROOT, 
        })
    )
    urlpatterns += append
    log.warn("Added file serve URLs to urls.py. This should only happen on non production systems.")