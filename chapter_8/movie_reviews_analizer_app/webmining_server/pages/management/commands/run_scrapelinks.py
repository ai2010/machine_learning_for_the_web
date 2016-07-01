from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from optparse import make_option
from pages.models import Page,SearchTerm
import os



class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
                make_option('--searchid',
                             dest='searchid', type='int',
                             action='store',
                             help=('id of the search term')),
                make_option('--num_reviews',
                             dest='num_reviews', type='int',
                             action='store',
                             help=('number of reviews to crawl')),
       )


    def handle(self, *args, **options):
         searchid = int(options['searchid'])
         num_reviews = options['num_reviews']
         if num_reviews == None:
            #default
            num_reviews = 5
         #print num_reviews

         s = SearchTerm.objects.get(id=searchid)       
         pages = s.pages.all().filter(review=True)
         urls = []
         for u in pages:
             urls.append(u.url)
         #crawl
         #print settings.BASE_DIR
         cmd = 'cd '+settings.BASE_DIR+'../scrapy_spider & scrapy crawl scrapy_spider_recursive -a url_list=%s -a search_id=%s' %('\"'+str(','.join(urls[:num_reviews]).encode('utf-8'))+'\"','\"'+str(searchid)+'\"')
         print 'cmd:',cmd
         os.system(cmd)