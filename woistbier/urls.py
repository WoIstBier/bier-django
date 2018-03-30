from django.conf.urls import url, include
from django.views.generic import TemplateView
import woistbier_rest.views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import logging
log = logging.getLogger(__name__)
import socket
if  not 'cepheus' in socket.gethostname():
    LOCALHOST = True
else:
    LOCALHOST = False

urlpatterns = [

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', 'django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/?', admin.site.urls),

    #include the urls from the polls app.
    url('bier/?', include('woistbier_rest.urls')),

    url(r'^$', woistbier_rest.views.index),

    #url(r'^$', 'woistbier_rest.views.index', name="index"),
    url(r'^about/?',
        TemplateView.as_view(template_name='bier/contact.html'),
        name='about'),
    url(r'^beer/?',
        TemplateView.as_view(template_name='bier/beer.html'),
        name='beer'),
    url(r'^impressum/?',
        TemplateView.as_view(template_name='bier/impressum.html'),
        name='impressum'),
    url(r'^api-auth/', include('rest_framework.urls')),
]

handler404 = 'woistbier_rest.views.not_found_view'

if LOCALHOST:
    print('You are running on LOCALHOST.')
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    #from django.conf import settings
    # append= [ '',
    #     url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    #         'document_root': settings.MEDIA_ROOT,
    #     }),
    #     url(r'^static/(?P<path>.*)$','django.views.static.serve',{
    #         'document_root': settings.STATIC_ROOT,
    #     })
    # ]
    # urlpatterns += append
    log.warn("Added file serve URLs to urls.py. This should only happen on non production systems!.")
