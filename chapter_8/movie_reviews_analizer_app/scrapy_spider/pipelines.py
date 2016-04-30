# -*- coding: utf-8 -*-

class ReviewPipeline(object):
    def process_item(self, item, spider):
        #if spider.name == 'scrapy_spider_reviews':#not working
           item.save()
           return item
'''
class RecursivePipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'scrapy_spider_recursive':
           item.save()
           return item
'''