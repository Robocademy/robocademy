from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('about.views',
    (r'^$', direct_to_template, {'template': 'about/index.html', 'extra_context': {'page': 'about'}}),
    (r'^contributors/$', 'contributors'),
)