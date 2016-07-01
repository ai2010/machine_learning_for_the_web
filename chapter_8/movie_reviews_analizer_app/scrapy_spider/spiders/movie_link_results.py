'''
usage: scrapy runspider recursive_link_results.py (or from root folder: scrapy crawl scrapy_spider_reviews)
'''


from newspaper import Article
from urlparse import urlparse
from scrapy.selector import Selector
from scrapy import Spider
from scrapy.spiders import BaseSpider,CrawlSpider, Rule
from scrapy.http import Request

from scrapy_spider import settings
from scrapy_spider.items import PageItem,SearchItem

unwanted_domains = ['youtube.com','www.youtube.com']
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))

def CheckQueryinReview(keywords,title,content):
    print keywords
    content_list = map(lambda x:x.lower(),content.split(' '))
    title_list = map(lambda x:x.lower(),title.split(' '))
    words = content_list+title_list
    for k in keywords:
        if k in words:
            return True
    return False


class Search(Spider):

    # Parameters set used for spider crawling
    name = 'scrapy_spider_reviews'
    
    def __init__(self,url_list,search_key):#specified by -a
        print settings.BASE_DIR
        self.search_key = search_key
        self.keywords = [w.lower() for w in search_key.split(" ") if w not in stopwords]
        print url_list
        self.start_urls =url_list.split(',')#['http://www.allmovie.com/blog/post/the-martian-the-allmovie-review']
        print len(self.start_urls)
        #allowed_domains = ['www.rottentomatoes.com','www.firstpost.com','www.theguardian.com','www.mirror.co.uk','www.comingsoon.net','www.independent.co.uk','www.newsok.com,'www.standard.co.uk','www.ew.com','www.heraldscotland.com','www.cnn.com','www.belfasttelegraph.co.uk','www.wsj.com','www.dailystar.co.uk','www.ibtimes.co.uk','www.denverpost.com','www.abcnews.go.com','www.radiotimes.com','www.latimes.com','www.telegraph.co.uk','artsbeat.blogs.nytimes.com','www.irishtimes.com','www.digitalspy.co.uk','www.digitaltrends.com','www.dailymail.co.uk','www.newsday.com','www.philadelphia.cbslocal.com','www.cbsnews.com','www.thewrap.com','www.rollingstone.com','www.movieweb.com','www.avclub.com','www.freebeacon.com','news.nationalpost.com','www.usatoday.com','www.deadline.com','www.nytimes.com','www.chicagotribune.com','www.amny.com','www.oregonlive.com','www.hollywoodreporter.com','www.celluloidcinema.com','hollywoodlife.com']
        
        super(Search, self).__init__(url_list)
    
    def start_requests(self):
        for url in self.start_urls:
            print('request',url)
            yield Request(url=url, callback=self.parse_site,dont_filter=True)
            #yield self.make_requests_from_url(url)
                        
    def parse_site(self, response):
        ## Get the selector for xpath parsing or from newspaper
        
        
        def crop_emptyel(arr):
            return [u for u in arr if u!=' ']
        
        domain = urlparse(response.url).hostname
        a = Article(response.url)
        a.download()
        a.parse()
        ## Get meta info from website
        title = a.title.encode('ascii','ignore').replace('\n','')
        
        sel = Selector(response)
        if title==None:
            title = sel.xpath('//title/text()').extract()
            if len(title)>0:
                title = title[0].encode('utf-8').strip().lower()
                
        content = a.text.encode('ascii','ignore').replace('\n','')
        if content == None:
            content = 'none'
            if len(crop_emptyel(sel.xpath('//div//article//p/text()').extract()))>1:
                contents = crop_emptyel(sel.xpath('//div//article//p/text()').extract())
                print 'divarticle'
            elif len(crop_emptyel(sel.xpath('//article[contains(@class,"article")]//p/text()').extract()))>1:
                print 'article'
                contents = crop_emptyel(sel.xpath('//article[contains(@class,"article")]//p/text()').extract()) 
            elif len(crop_emptyel(sel.xpath('//div[contains(@id,"content")]//p/text()').extract()))>1:
                print '3'
                contents = crop_emptyel(sel.xpath('//div[contains(@id,"content")]//p/text()').extract())
            elif len(crop_emptyel(sel.xpath('//div[contains(@class,"body")]//p/text()').extract()))>1:
                print '4'
                contents = crop_emptyel(sel.xpath('//div[contains(@class,"body")]//p/text()').extract())
            elif len(crop_emptyel(sel.xpath('//section[contains(@class,"text")]//p/text()').extract()))>1:
                print '6'
                contents = crop_emptyel(sel.xpath('//section[contains(@class,"text")]//p/text()').extract())
            elif len(crop_emptyel(sel.xpath('//div[contains(@itemprop,"article")]//p/text()').extract()))>0:
                print '7'
                contents = crop_emptyel(sel.xpath('//div[contains(@itemprop,"article")]//p/text()').extract())
            elif len(crop_emptyel(sel.xpath('//div//article[contains(@itemprop,"article")]//p/text()').extract()))>1:
                contents = crop_emptyel(sel.xpath('//div//article[contains(@itemprop,"article")]//p/text()').extract())
            elif len(crop_emptyel(sel.xpath('//div[contains(@id,"description")]//span/text()').extract()))>1:
                print 'descr'
                contents = crop_emptyel(sel.xpath('//div[contains(@id,"description")]//span/text()').extract())
            elif len(crop_emptyel(sel.xpath('//div[contains(@class,"article")]//div/text()').extract()))>1:
                print 'div contains article'
                contents = crop_emptyel(sel.xpath('//div[contains(@class,"article")]//div/text()').extract())
            elif len(crop_emptyel(sel.xpath('//div[contains(@class,"article")]//p/text()').extract()))>1:
                print '2'
                contents = crop_emptyel(sel.xpath('//div[contains(@class,"article")]//p/text()').extract())
            elif len(crop_emptyel(sel.xpath('//p[contains(@class,"lead")]//text()').extract()))>0:
                print '5'
                contents = crop_emptyel(sel.xpath('//p[contains(@class,"lead")]//text()').extract())
            elif len(crop_emptyel(sel.xpath('//div[contains(@class,"text")]//p/text()').extract()))>0:
                print '1'
                contents = crop_emptyel(sel.xpath('//div[contains(@class,"text")]//p/text()').extract())
            elif len(crop_emptyel(sel.xpath('/html/head/meta[@name="description"]/@content').extract()))>0:
                contents = crop_emptyel(sel.xpath('/html/head/meta[@name="description"]/@content').extract())
            content = ' '.join([c.encode('utf-8') for c in contents]).strip().lower()
        print 'title:',title
        #print 'content:',content
                
        #get search item 
        search_item = SearchItem.django_model.objects.get(term=self.search_key)
        #save item
        if not PageItem.django_model.objects.filter(url=response.url).exists():
            if len(content) > 0:
                if CheckQueryinReview(self.keywords,title,content):
                    if domain not in unwanted_domains:
                        newpage = PageItem()
                        newpage['searchterm'] = search_item
                        newpage['title'] = title
                        newpage['content'] = content
                        newpage['url'] = response.url
                        newpage['depth'] = 0
                        newpage['review'] = True
                        #newpage.save()
                        return newpage  
        else:
            return null      
        '''
        search_links_list =  sel.xpath('//h3/a/@href').extract()
        search_links_list = [re.search('q=(.*)&sa',n).group(1) for n in search_links_list if re.search('q=(.*)&sa',n)]
        print 'num-sites:',len(search_links_list)
        ## Display a list of the result link,scrape each link to extract content,title
        for n in search_links_list:
            print 'site:',n
        '''
        
        

