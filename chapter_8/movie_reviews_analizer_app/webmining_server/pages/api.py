from rest_framework import views,generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from pages.serializers import SearchTermSerializer
from pages.models import SearchTerm,Page


#REMARK: 
#the page_size has to be set up from the LargeResultsSetPagination
#to avoid that the call collect partial results!!!!
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000
  
class SearchTermsList(generics.ListAPIView):

    serializer_class = SearchTermSerializer
    permission_classes = (AllowAny,)
    pagination_class = LargeResultsSetPagination
    
    def get_queryset(self):
        return SearchTerm.objects.all()  
        
class PageCounts(views.APIView):

    permission_classes = (AllowAny,)
    
    def get(self,*args, **kwargs):
        searchid=self.kwargs['pk']
        reviewpages = Page.objects.filter(searchterm=searchid).filter(review=True)
        npos = len([p for p in reviewpages if p.sentiment==1])
        nneg = len(reviewpages)-npos
        return Response({'npos':npos,'nneg':nneg})