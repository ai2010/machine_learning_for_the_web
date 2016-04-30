'''

#############################################
usage: scrapy runspider google_scraper_results.py (or from root folder: scrapy crawl scrapy_spider_google)

'''

import re
import os
import sys
import json
import string
import math
#import yaml
#from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.contrib.spiders import Spider,CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request

class Search(Spider):

    # Parameters set used for spider crawling
    name = 'scrapy_spider_google'
    
    
    def __init__(self,g_search_term):#specified by -a
        
        sp_search_url_list = []
        search_results_num = 100 #set to any variable 
        pages_to_scan = int(math.ceil(search_results_num/100.0)) 
        for n in range(0,pages_to_scan,1):
            prefix_of_search_text = "https://www.google.com/search?q="
            postfix_of_search_text = '&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:en-US:official&client=firefox-a&channel=fflb&num=100'# non changable text
            output_url_str = prefix_of_search_text + g_search_term + \
                              postfix_of_search_text +\
                              self.formed_page_num(n)
            sp_search_url_list.append(output_url_str)
        
        #self.name = 'scrapy_spyder'
        #self.allowed_domains = ['www.google.com']#no allowed_domains means ALL
        self.start_urls = sp_search_url_list#['http://www.allmovie.com/blog/post/the-martian-the-allmovie-review']
        print self.start_urls
        
    def parse(self, response):
        ## Get the selector for xpath parsing
        sel = Selector(response)
        google_search_links_list =  sel.xpath('//h3/a/@href').extract()
        google_search_links_list = [re.search('q=(.*)&sa',n).group(1) for n in google_search_links_list if re.search('q=(.*)&sa',n)]

        ## Display a list of the result link,scrape each link to extract content,title
        for n in google_search_links_list:
            print 'site:',n
            
        print 'num sites:',len(google_search_links_list)
        




    def formed_page_num(self, page_index):
        """ Method to form part of the url where the page num is included.
            Args:
                page_num (int): page num in int to be formed. Will convert to multiple of 100.
                for example page_index 1 will require "&start=100".
                Start page begin with index 0
            Returns:
                (str): return part of the url.

        """
        return "&start=%i" %(page_index*100)


