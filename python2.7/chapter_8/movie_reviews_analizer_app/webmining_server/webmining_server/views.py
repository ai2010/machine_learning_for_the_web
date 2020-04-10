import datetime
import os
import urllib2
import urllib
import numpy
import json
from django.shortcuts import render
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import loader
from django.core.cache import cache
from pages.models import Page,SearchTerm
from pgrank.pgrank import pgrank
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import collections
import logging



# Bing API key
API_KEY = "yourkeyhere"

#PARAMETERS
test_mode = False
num_reviews = 20
num_bestwords = 20000
stopwords = set(stopwords.words('english'))
method_selfeatures = 'best_words_features'

def about(request):
    return render(request, 'movie_reviews/about.html',
                          {'request': request})
                          
def bing_api(query):
    keyBing = API_KEY        # get Bing key from: https://datamarket.azure.com/account/keys
    credentialBing = 'Basic ' + (':%s' % keyBing).encode('base64')[:-1] # the "-1" is to remove the trailing "\n" which encode adds
    searchString = '%27X'+query.replace(" ",'+')+'movie+review%27'
    top = 50#maximum allowed by Bing
    
    reviews_urls = []
    if num_reviews<top:
        offset = 0
        url = 'https://api.datamarket.azure.com/Bing/Search/Web?' + \
              'Query=%s&$top=%d&$skip=%d&$format=json' % (searchString, num_reviews, offset)

        request = urllib2.Request(url)
        request.add_header('Authorization', credentialBing)
        requestOpener = urllib2.build_opener()
        response = requestOpener.open(request) 

        results = json.load(response)
        reviews_urls = [ d['Url'] for d in results['d']['results']]
    else:
        nqueries = int(float(num_reviews)/top)+1
        for i in xrange(nqueries):
            offset = top*i
            if i==nqueries-1:
                top = num_reviews-offset
                url = 'https://api.datamarket.azure.com/Bing/Search/Web?' + \
                      'Query=%s&$top=%d&$skip=%d&$format=json' % (searchString, top, offset)

                request = urllib2.Request(url)
                request.add_header('Authorization', credentialBing)
                requestOpener = urllib2.build_opener()
                response = requestOpener.open(request) 
            else:
                top=50
                url = 'https://api.datamarket.azure.com/Bing/Search/Web?' + \
                      'Query=%s&$top=%d&$skip=%d&$format=json' % (searchString, top, offset)

                request = urllib2.Request(url)
                request.add_header('Authorization', credentialBing)
                requestOpener = urllib2.build_opener()
                response = requestOpener.open(request)                
            results = json.load(response)
            reviews_urls += [ d['Url'] for d in results['d']['results']]
            
    print 'REVIEWS NUMBER:',len(reviews_urls)
    return reviews_urls

def parse_bing_results():
    file_data = open(os.path.dirname(__file__)+'/bing_the_martian_results.json','r')
    bing_json = json.load(file_data)
    print len(bing_json['d']['results'])
    reviews_urls = [ d['Url'] for d in bing_json['d']['results']]
    print reviews_urls
    return reviews_urls
            
def analyzer(request):
    context = {}

    if request.method == 'POST':
        post_data = request.POST
        query = post_data.get('query', None)
        if query:
            return redirect('%s?%s' % (reverse('webmining_server.views.analyzer'),
                                urllib.urlencode({'q': query})))   
    elif request.method == 'GET':
        get_data = request.GET
        query = get_data.get('q')
        if not query:
            return render_to_response(
                'movie_reviews/home.html', context)

        context['query'] = query
        stripped_query = query.strip().lower()
        urls = []
        
        if test_mode:
           urls = parse_bing_results()
        else:
           urls = bing_api(stripped_query)
           
        if len(urls)== 0:
           return render_to_response(
               'movie_reviews/noreviewsfound.html', context)
               
        print 'urls:',str(urls[:num_reviews])
        if not SearchTerm.objects.filter(term=stripped_query).exists():
           s = SearchTerm(term=stripped_query)
           s.save()
           try:
               #scrape
               cmd = 'cd ../scrapy_spider & scrapy crawl scrapy_spider_reviews -a url_list=%s -a search_key=%s' %('\"'+str(','.join(urls[:num_reviews]).encode('utf-8'))+'\"','\"'+str(stripped_query)+'\"')
               print 'cmd:',cmd
               os.system(cmd)
           except:
               print 'error!'
               s.delete()
        else:
           #collect the pages already scraped 
           s = SearchTerm.objects.get(term=stripped_query)
           
        #calc num pages
        pages = s.pages.all().filter(review=True)
        if len(pages) == 0:
           s.delete()
           return render_to_response(
               'movie_reviews/noreviewsfound.html', context)
               
        s.num_reviews = len(pages)
        s.save()
         
        context['searchterm_id'] = int(s.id)


        #train classifier with nltk
        def train_clf(method):
            negidxs = movie_reviews.fileids('neg')
            posidxs = movie_reviews.fileids('pos')
            if method=='stopword_filtered_words_features':
                negfeatures = [(stopword_filtered_words_features(movie_reviews.words(fileids=[file])), 'neg') for file in negidxs]
                posfeatures = [(stopword_filtered_words_features(movie_reviews.words(fileids=[file])), 'pos') for file in posidxs]
            elif method=='best_words_features':
                negfeatures = [(best_words_features(movie_reviews.words(fileids=[file])), 'neg') for file in negidxs]
                posfeatures = [(best_words_features(movie_reviews.words(fileids=[file])), 'pos') for file in posidxs]
            elif method=='best_bigrams_words_features':
                negfeatures = [(best_bigrams_words_features(movie_reviews.words(fileids=[file])), 'neg') for file in negidxs]
                posfeatures = [(best_bigrams_words_features(movie_reviews.words(fileids=[file])), 'pos') for file in posidxs]
                
            trainfeatures = negfeatures + posfeatures
            clf = NaiveBayesClassifier.train(trainfeatures)
            return clf
            
        def stopword_filtered_words_features(words):
            return dict([(word, True) for word in words if word not in stopwords])
 
        #Eliminate Low Information Features
        def GetHighInformationWordsChi(num_bestwords):
            word_fd = FreqDist()
            label_word_fd = ConditionalFreqDist()
 
            for word in movie_reviews.words(categories=['pos']):
                word_fd[word.lower()] +=1
                label_word_fd['pos'][word.lower()] +=1
 
            for word in movie_reviews.words(categories=['neg']):
                word_fd[word.lower()] +=1
                label_word_fd['neg'][word.lower()] +=1
 
            pos_word_count = label_word_fd['pos'].N()
            neg_word_count = label_word_fd['neg'].N()
            total_word_count = pos_word_count + neg_word_count
 
            word_scores = {}
 
            for word, freq in word_fd.iteritems():
                pos_score = BigramAssocMeasures.chi_sq(label_word_fd['pos'][word],
                    (freq, pos_word_count), total_word_count)
                neg_score = BigramAssocMeasures.chi_sq(label_word_fd['neg'][word],
                    (freq, neg_word_count), total_word_count)
                word_scores[word] = pos_score + neg_score
 
            best = sorted(word_scores.iteritems(), key=lambda (w,s): s, reverse=True)[:num_bestwords]
            bestwords = set([w for w, s in best])
            return bestwords
            
        bestwords = cache.get('bestwords')
        if bestwords == None:
            bestwords = GetHighInformationWordsChi(num_bestwords)
        def best_words_features(words):
            return dict([(word, True) for word in words if word in bestwords])
        
        def best_bigrams_words_features(words, measure=BigramAssocMeasures.chi_sq, nbigrams=200):
            bigram_finder = BigramCollocationFinder.from_words(words)
            bigrams = bigram_finder.nbest(measure, nbigrams)
            d = dict([(bigram, True) for bigram in bigrams])
            d.update(best_words_features(words))
            return d
 
        clf = cache.get('clf')
        if clf == None:
            clf = train_clf(method_selfeatures)

        cntpos = 0
        cntneg = 0
        for p in pages:
            words = p.content.split(" ")
            feats = best_words_features(words)#bigram_word_features(words)#stopword_filtered_word_feats(words)
            #print feats
            str_sent = clf.classify(feats)
            if str_sent == 'pos':
               p.sentiment = 1
               cntpos +=1
            else:
               p.sentiment = -1
               cntneg +=1
            p.save()

        context['reviews_classified'] = len(pages)
        context['positive_count'] = cntpos
        context['negative_count'] = cntneg
        context['classified_information'] = True

    return render_to_response(
        'movie_reviews/home.html', context)

def pgrank_view(request,pk): 
    context = {}
    get_data = request.GET
    scrape = get_data.get('scrape','False')
    s = SearchTerm.objects.get(id=pk)
    
    if scrape == 'True':
        pages = s.pages.all().filter(review=True)
        urls = []
        for u in pages:
            urls.append(u.url)
        #crawl
        cmd = 'cd ../scrapy_spider & scrapy crawl scrapy_spider_recursive -a url_list=%s -a search_id=%s' %('\"'+str(','.join(urls[:]).encode('utf-8'))+'\"','\"'+str(pk)+'\"')
        print 'cmd:',cmd
        os.system(cmd)

    links = s.links.all()
    if len(links)==0:
       context['no_links'] = True
       return render_to_response(
           'movie_reviews/pg-rank.html', context)
    #calc pgranks
    pgrank(pk)
    #load pgranks in descending order of pagerank
    pages_ordered = s.pages.all().filter(review=True).order_by('-new_rank')
    context['pages'] = pages_ordered
    
    return render_to_response(
        'movie_reviews/pg-rank.html',  context)