from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('devices.views',
    url(r'^connections/$', 'device_connections'),
    url(r'^connections/json/$', 'device_connections_json'),
    url(r'^arduino/send_code/$', 'send_code'),
    url(r'^arduino/get_code/(?P<connection_id>)/$', 'get_code'),
    url(r'^arduino/get_status/(?P<connection_id>)/$', 'get_status'),
    url(r'^arduino/set_status/(?P<connection_id>)/$', 'set_status'),
    url(r'^arduino/get_cmd_status/(?P<connection_id>)/$', 'get_cmd_status'),
    url(r'^arduino/set_cmd_status/$', 'set_cmd_status'),
    url(r'^arduino/get_serial_monitor/(?P<connection_id>)/$', 'get_serial_monitor'),
    url(r'^arduino/set_serial_monitor/$', 'set_serial_monitor'),
    url(r'^arduino/save_example/$', 'save_example'),
    url(r'^arduino/get_example_code/(?P<connection_id>)/$', 'get_example_code'),
)