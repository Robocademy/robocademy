from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('interactive_courses.views',
    url(r'^$', 'index'),
    url(r'^(?P<course_slug>[\w_]+)/$', 'course'),
    url(r'^(?P<course_slug>[\w_]+)/embed/$', 'course_embed'),
)