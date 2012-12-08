from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('devices.views',
    url(r'^connections/$', 'device_connections'),
    url(r'^connections/json/$', 'device_connections_json'),
)