import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import collections
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.core.cache import cache

stopwords = set(stopwords.words('english'))

method_selfeatures = 'best_words_features'

'''
python manage.py load_sentimentclassifier --num_bestwords=20000
'''

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
                make_option('-n', '--num_bestwords',
                             dest='num_bestwords', type='int',
                             action='store',
                             help=('number of words with high information')),
       )



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
        

    def stopword_filtered_words_features(self,words):
        return dict([(word, True) for word in words if word not in stopwords])

    #eliminate Low Information Features
    def GetHighInformationWordsChi(self,num_bestwords):
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

    def best_words_features(self,words):
        return dict([(word, True) for word in words if word in self.bestwords])
    
    def best_bigrams_word_features(self,words, measure=BigramAssocMeasures.chi_sq, nbigrams=200):
        bigram_finder = BigramCollocationFinder.from_words(words)
        bigrams = bigram_finder.nbest(measure, nbigrams)
        d = dict([(bigram, True) for bigram in bigrams])
        d.update(best_words_features(words))
        return d
    
    def handle(self, *args, **options):
         num_bestwords = options['num_bestwords']
         
         self.bestwords = self.GetHighInformationWordsChi(num_bestwords)
         clf = self.train_clf(method_selfeatures)
         cache.set('clf',clf)
         cache.set('bestwords',self.bestwords)