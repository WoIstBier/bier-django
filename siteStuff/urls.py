from django.conf.urls import patterns, include, url
from settings import MEDIA_ROOT, STATIC_ROOT

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

    url(r'^$', 'bier.views.index', name='kiosk')
)

if LOCALHOST:
    append= patterns( '',  
        url(r'^bier/media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT,
        }),
        url(r'^bier/static/(?P<path>.*)$','django.views.static.serve',{
            'document_root': STATIC_ROOT, 
        })
    )
    urlpatterns += append
    log.warn("Added file serve URLs to urls.py. This should only happen on non production systems.")