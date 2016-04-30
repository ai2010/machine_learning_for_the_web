from pages.models import SearchTerm
from rest_framework import serializers
        
class SearchTermSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = SearchTerm
        fields = ('id', 'term')
