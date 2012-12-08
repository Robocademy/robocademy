from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('courses.views',
    url(r'^arduino/$', 'arduino'),
    url(r'^arduino_expert/$', 'arduino_expert'),
    url(r'^arduino/send_code/$', 'send_code'),
    url(r'^arduino/get_code/$', 'get_code'),
    url(r'^arduino/get_status/$', 'get_status'),
    url(r'^arduino/set_status/$', 'set_status'),
    url(r'^arduino/get_cmd_status/$', 'get_cmd_status'),
    url(r'^arduino/set_cmd_status/$', 'set_cmd_status'),
    url(r'^arduino/get_serial_monitor/$', 'get_serial_monitor'),
    url(r'^arduino/set_serial_monitor/$', 'set_serial_monitor'),
    url(r'^arduino/save_example/$', 'save_example'),
    url(r'^arduino/get_example_code/$', 'get_example_code'),
    url(r'^arduino/test_code/$', 'test_code'),
    url(r'^arduino/get_lessons/(?P<device_configuration_id>\d+)/$', 'get_lessons'),
)