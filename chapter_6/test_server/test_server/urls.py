from django.conf.urls import patterns, include, url
from django.contrib import admin
from addressesapp.api import AddressesList


urlpatterns = patterns('',
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^$','addressesapp.views.main'),
    url(r'^book/','addressesapp.views.addressesbook',name='addressesbook'),
    url(r'^delete/(?P<name>.*)/','addressesapp.views.delete_person', name='delete_person'),
    url(r'^book-search/','addressesapp.views.get_contacts', name='get_contacts'),
    url(r'^addresses-list/', AddressesList.as_view(), name='addresses-list'),
    url(r'^notfound/','addressesapp.views.notfound',name='notfound'),
    url(r'^admin/', include(admin.site.urls)),
)
