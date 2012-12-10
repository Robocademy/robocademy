from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('courses.views',
    #url(r'^arduino/$', 'arduino'),
    url(r'^arduino_expert/$', 'arduino_expert'),

)