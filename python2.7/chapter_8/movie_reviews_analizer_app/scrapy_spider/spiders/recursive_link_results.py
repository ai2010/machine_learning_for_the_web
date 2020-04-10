'''
usage: scrapy runspider recursive_link_results.py (or from root folder: scrapy crawl scrapy_spyder_recursive)
'''

#from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

from scrapy_spider.items import PageItem,LinkItem,SearchItem


class Search(CrawlSpider):

    # Parameters set used for spider crawling
    name = 'scrapy_spider_recursive'
    
    def __init__(self,url_list,search_id):#specified by -a
    
        #REMARK is allowed_domains is not set then ALL are allowed
        self.start_urls = url_list.split(',')
        self.search_id = int(search_id)
        
        #allow any link but the ones with different font size(repetitions)
        self.rules = (
            Rule(LinkExtractor(allow=(),deny=('fontSize=*','infoid=*','SortBy=*', ),unique=True), callback='parse_item', follow=True), 
            )
        super(Search, self).__init__(url_list)

    def parse_item(self, response):
        sel = Selector(response)
        
        ## Get meta info from website
        title = sel.xpath('//title/text()').extract()
        if len(title)>0:
            title = title[0].encode('utf-8')
            
        contents = sel.xpath('/html/head/meta[@name="description"]/@content').extract()
        content = ' '.join([c.encode('utf-8') for c in contents]).strip()

        fromurl = response.request.headers['Referer']
        tourl = response.url
        depth = response.request.meta['depth']
        
        #get search item 
        search_item = SearchItem.django_model.objects.get(id=self.search_id)
        #newpage
        if not PageItem.django_model.objects.filter(url=tourl).exists():
            newpage = PageItem()
            newpage['searchterm'] = search_item
            newpage['title'] = title
            newpage['content'] = content
            newpage['url'] = tourl
            newpage['depth'] = depth
            newpage.save()#cant use pipeline cause the execution can finish here
            
        print fromurl,'--title:',title,'-',response.url,' depth:',depth
        #print contents
        #if( int(depth)> 1):
        #   print fromurl,'--title:',title,'-',response.url,' depth:',depth
        
        #get from_id,to_id
        from_page = PageItem.django_model.objects.get(url=fromurl)
        from_id = from_page.id
        to_page = PageItem.django_model.objects.get(url=tourl)
        to_id = to_page.id

        

        
        #newlink
        if not LinkItem.django_model.objects.filter(from_id=from_id).filter(to_id=to_id).exists():
            newlink = LinkItem()
            newlink['searchterm'] = search_item
            newlink['from_id'] = from_id
            newlink['to_id'] = to_id
            newlink.save()
        


