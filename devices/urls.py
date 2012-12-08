from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('devices.views',
    url(r'^connections/$', 'device_connections'),
    url(r'^connections/json/$', 'device_connections_json'),
    url(r'^send_code/$', 'send_code'),
    url(r'^get_code/(?P<connection_id>)/$', 'get_code'),
    url(r'^get_status/(?P<connection_id>)/$', 'get_status'),
    url(r'^set_status/(?P<connection_id>)/$', 'set_status'),
    url(r'^get_cmd_status/(?P<connection_id>)/$', 'get_cmd_status'),
    url(r'^set_cmd_status/$', 'set_cmd_status'),
    url(r'^get_serial_monitor/(?P<connection_id>)/$', 'get_serial_monitor'),
    url(r'^set_serial_monitor/$', 'set_serial_monitor'),
    url(r'^save_example/$', 'save_example'),
    url(r'^get_example_code/(?P<connection_id>)/$', 'get_example_code'),
)