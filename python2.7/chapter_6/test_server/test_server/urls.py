from django.conf.urls import include, url
from django.contrib import admin
from addressesapp.api import AddressesList
from addressesapp.views import main, get_contacts, addressesbook, delete_person, notfound

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='API name')
urlpatterns = [
    url(r'^docs/', schema_view)
]  
urlpatterns += [
    #url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^$',main, name='home'),
    url(r'^book/',addressesbook,name='addressesbook'),
    url(r'^delete/(?P<name>.*)/',delete_person, name='delete_person'),
    url(r'^book-search/',get_contacts, name='get_contacts'),
    url(r'^addresses-list/', AddressesList.as_view(), name='addresses-list'),
    url(r'^notfound/',notfound, name='notfound'),
    url(r'^admin/', include(admin.site.urls)),
]
