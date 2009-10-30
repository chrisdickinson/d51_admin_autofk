from django.conf.urls.defaults import patterns, url
from resource import simplemodel_resource

urlpatterns = patterns(
    '',
    url(r'^api/$', simplemodel_resource, {'emitter_format':'json'}, name='simplemodel-json')
)
