from pages.models import Link,Page,SearchTerm
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option





class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
                make_option('-s', '--searchid',
                             dest='searchid', type='int',
                             action='store',
                             help=('id of the search term to delete')),
       )


    def handle(self, *args, **options):
         searchid = options['searchid']
         if searchid == None:
             print "please specify searchid: python manage.py --searchid=--"
             #list
             for sobj in SearchTerm.objects.all():
                 print 'id:',sobj.id,"  term:",sobj.term
         else:
             print 'delete...'
             search_obj = SearchTerm.objects.get(id=searchid)
             pages = search_obj.pages.all()
             pages.delete()
             links = search_obj.links.all()
             links.delete()
             search_obj.delete()