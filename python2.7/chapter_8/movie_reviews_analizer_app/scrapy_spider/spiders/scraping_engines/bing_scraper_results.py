'''

#############################################
usage: scrapy runspider bing_scraper_results.py
or: scrapy crawl scrapy_spider_bing
'''

import re
import os
import sys
import json
import string
#import yaml
#from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request

#from webmining.pages.models import Page,Links

class Search(CrawlSpider):

    # Parameters set used for spider crawling
    name = 'scrapy_spider_bing'
    
    #allowed_domains = ['www.bing.com']
    start_urls = ['https://www.bing.com/search?q=the+martian+review']
    #allow any link but the ones with different font size(repetitions)
    rules = (
        Rule(LinkExtractor(allow=('',),deny=('fontSize=*','infoid=*','SortBy=*', ),unique=True), callback='parse_item', follow=True), 
        )

    def parse_item(self, response):
            print 
            print 'general website processing',(len(self.start_urls))
            sel = Selector(response)

            ## Get meta info from website
            title = sel.xpath('//title/text()').extract()
            if len(title)>0:
                title = title[0].encode(errors='replace') #replace any unknown character with ?
            contents = sel.xpath('/html/head/meta[@name="description"]/@content').extract()
            if len(contents)>0:
                contents = contents[0].encode(errors='replace') #replace any unknown character with ?
            #response.xpath('//div[contains(@class,"text")]').extract()
            #response.xpath('//div[contains(@class,"text")]//p/text()').extract()
            #response.xpath('//div[contains(@class,"text")]//p/node()').extract()
            fromurl = response.request.headers['Referer']
            tourl = response.url
            depth = response.request.meta['depth']
            
            #page = Page()
            print fromurl,'--title:',title,'-',response.url,' depth:',depth
            print contents
            if( int(depth)> 1):
               print fromurl,'--title:',title,'-',response.url,' depth:',depth







