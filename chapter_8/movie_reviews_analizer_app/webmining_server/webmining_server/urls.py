from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from rest_framework import routers
from pages.api  import PageCounts,SearchTermsList
#router = routers.DefaultRouter()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^$','webmining_server.views.analyzer'),
    url(r'^pg-rank/(?P<pk>\d+)/','webmining_server.views.pgrank_view', name='pgrank_view'),
    url(r'^pages-sentiment/(?P<pk>\d+)/', PageCounts.as_view(), name='pages-sentiment'),
    url(r'^search-list/', SearchTermsList.as_view(), name='search-list'),
    url(r'^about/','webmining_server.views.about'),
    (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
