# -*- coding: utf-8 -*-

import os
BOT_NAME = 'scrapy_spider'

SPIDER_MODULES = ['scrapy_spider.spiders']
NEWSPIDER_MODULE = 'scrapy_spider.spiders'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Setting up django's project full path.
import sys
#sys.path.insert(0, '/Users/andrea/Desktop/book_packt/chapters/web mining/movie_reviews_analizer_app/webmining')
sys.path.insert(0, BASE_DIR+'/webmining_server')
# Setting up django's settings module name.
os.environ['DJANGO_SETTINGS_MODULE'] = 'webmining_server.settings'
#import django to load models(otherwise AppRegistryNotReady: Models aren't loaded yet):
import django
django.setup()

ITEM_PIPELINES = {
    'scrapy_spider.pipelines.ReviewPipeline': 1000,
}

#DOWNLOAD_DELAY = 0.5 
DEPTH_LIMIT = 2
LOG_ENABLED=False

#get faster
CONCURRENT_REQUESTS = 5000
CONCURRENT_REQUESTS_PER_DOMAIN = 3000
CONCURRENT_ITEMS = 200
