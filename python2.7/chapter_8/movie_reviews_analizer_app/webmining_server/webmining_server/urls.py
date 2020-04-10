#from django.conf.urls import patterns, include, url
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from pages.api  import PageCounts,SearchTermsList
import webmining_server.views
#router = routers.DefaultRouter()
from webmining_server.views import analyzer,pgrank_view,about
from django.views.static import serve

'''
#django 1.7
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^$','webmining_server.views.analyzer'),
    url(r'^pg-rank/(?P<pk>\d+)/','webmining_server.views.pgrank_view', name='pgrank_view'),
    url(r'^pages-sentiment/(?P<pk>\d+)/', PageCounts.as_view(), name='pages-sentiment'),
    url(r'^search-list/', SearchTermsList.as_view(), name='search-list'),
    url(r'^about/','webmining_server.views.about'),
    url(r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
'''

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='API name')
urlpatterns = [
    url(r'^docs/', schema_view)
]

urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',analyzer),
    url(r'^pg-rank/(?P<pk>\d+)/',pgrank_view, name='pgrank_view'),
    url(r'^pages-sentiment/(?P<pk>\d+)/', PageCounts.as_view(), name='pages-sentiment'),
    url(r'^search-list/', SearchTermsList.as_view(), name='search-list'),
    url(r'^about/',about),
    url(r'^assets/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]