from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import os
from django.conf import settings

urlpatterns = patterns('',
    #url(r'^$', direct_to_template, {'template': 'index.html'}),
    url(r'^$', RedirectView.as_view(url='/courses/arduino/')),
    (r'^login/', 'about.views.loginuser'),
    (r'^createuser/', 'about.views.createuser'),
    (r'^about/', direct_to_template, {'template': 'about/index.html', 'extra_context': {'page': 'about'}}),
    (r'^courses/', include('courses.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(settings.PROJECT_ROOT, 'static/css')}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(settings.PROJECT_ROOT, 'static/images')}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(settings.PROJECT_ROOT, 'static/js')}),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
