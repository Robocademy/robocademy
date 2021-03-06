from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from django.views.generic import RedirectView
from django.views.generic.simple import redirect_to
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import os
from django.conf import settings

urlpatterns = patterns('',
    #url(r'^$', direct_to_template, {'template': 'index.html'}),
    (r'^get_dropdown_tree/$', 'devices.views.get_dropdown_tree'),
    url(r'^new_interface/$', direct_to_template, {'template': 'courses/new_interface.html'}),
    url(r'^$', 'courses.views.arduino_expert'),
    (r'^(?P<war_type>education|robot)_war/', 'wars.views.get_war_info'),
    (r'^login/', 'about.views.loginuser'),
    (r'^neil/', RedirectView.as_view(url='/interactive_courses/photography_101/admin/')),
    (r'^createuser/', 'about.views.createuser'),
    (r'^about/', include('about.urls')),
    #(r'^courses/', include('courses.urls')),
    (r'^courses[\w\d]*', RedirectView.as_view(url='/')),
    (r'^devices/', include('devices.urls')),
    (r'^interactive_courses/', include('interactive_courses.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'market/', include('market.urls')),

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
