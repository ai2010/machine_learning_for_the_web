from addressesapp.models import Person
from rest_framework import serializers


class AddressesSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Person
        fields = ('id', 'name', 'mail')
