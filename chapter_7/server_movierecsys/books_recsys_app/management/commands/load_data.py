from django.core.management.base import BaseCommand
import os
import optparse
import numpy as np
import pandas as pd
import math
import json
import copy
from BeautifulSoup import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
tknzr = WordPunctTokenizer()
#nltk.download('stopwords')
stoplist = stopwords.words('english')
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
from sklearn.feature_extraction.text import TfidfVectorizer
from books_recsys_app.models import MovieData
from django.core.cache import cache



#python manage.py load_data --input=plots.csv --nmaxwords=30000  --umatrixfile=umatrix.csv
class Command(BaseCommand):

    '''
    option_list = BaseCommand.option_list + (
            optparse.make_option('-i', '--input', dest='input',
                                 type='string', action='store',
                                 help=('Input plots file')),
            optparse.make_option('--nmaxwords', '--nmaxwords', dest='nmaxwords',
                                 type='int', action='store',
                                 help=('nmaxwords')),
            optparse.make_option('--umatrixfile', '--umatrixfile', dest='umatrixfile',
                                 type='string', action='store',
                                 help=('umatrixfile')),                                                               
        )
    '''
    
    def add_arguments(self, parser):

            parser.add_argument(
                '--input',
            action='store',
            help='Input plots file')
            
            parser.add_argument(
                '--nmaxwords',
            action='store',
            type = int,
            help='nmaxwords')
            
            parser.add_argument(
                '--umatrixfile',
            action='store',
            help='umatrixfile')
            
        
    def PreprocessTfidf(self,texts,stoplist=[],stem=False):
        newtexts = []
        for i in xrange(len(texts)):
            text = texts[i]
            if stem:
               tmp = [w for w in tknzr.tokenize(text) if w not in stoplist]
            else:
               tmp = [stemmer.stem(w) for w in [w for w in tknzr.tokenize(text) if w not in stoplist]]
            newtexts.append(' '.join(tmp))
        return newtexts
    
    def handle(self, *args, **options):
        input_file = options['input']
        
        df = pd.read_csv(input_file)
        tot_textplots = df['plot'].tolist()
        tot_titles = df['title'].tolist()
        nmaxwords=options['nmaxwords']
        vectorizer = TfidfVectorizer(min_df=0,max_features=nmaxwords)
        processed_plots = self.PreprocessTfidf(tot_textplots,stoplist,True)
        mod_tfidf = vectorizer.fit(processed_plots)
        vec_tfidf = mod_tfidf.transform(processed_plots)
        ndims = len(mod_tfidf.get_feature_names())
        nmovies = len(tot_titles[:])
        
        #delete all data
        MovieData.objects.all().delete()
        
        matr = np.empty([1,ndims])
        print ndims
        titles = []
        cnt=0
        for m in xrange(nmovies):
            moviedata = MovieData()
            moviedata.title=tot_titles[m]
            moviedata.description=tot_textplots[m]
            moviedata.ndim= ndims
            moviedata.array=json.dumps(vec_tfidf[m].toarray()[0].tolist())
            moviedata.save()
            newrow = json.loads(moviedata.array)
            if cnt==0:
                matr[0]=newrow
            else:
                matr = np.vstack([matr, newrow])
            titles.append(moviedata.title)
            cnt+=1
        #cached
        cache.set('data', matr)
        cache.set('titles', titles)
        titles = cache.get('titles')
        #print titles
        print 'len:',len(titles)
        cache.set('model',mod_tfidf)

        
        #load the utility matrix
        umatrixfile = options['umatrixfile']
        df_umatrix = pd.read_csv(umatrixfile)
        Umatrix = df_umatrix.values[:,1:]
        print 'umatrix:',Umatrix.shape
        cache.set('umatrix',Umatrix)
        #load rec methods... 
        cf_itembased = CF_itembased(Umatrix)
        cache.set('cf_itembased',cf_itembased)
        llr = LogLikelihood(Umatrix,titles)
        cache.set('loglikelihood',llr)
        
        
        #test...
        model_vec = cache.get('model')
        #print 'mod:',model_vec,'--',mod_tfidf
        print 'nwords:',len(model_vec.get_feature_names())
        #print 'vec:',model_vec.transform(['wars star'])  
        
from scipy.stats import pearsonr
from scipy.spatial.distance import cosine 
def sim(x,y,metric='cos'):
    if metric == 'cos':
       return 1.-cosine(x,y)
    else:#correlation
       return pearsonr(x,y)[0]
       
class CF_itembased(object):
    def __init__(self,data):
        #calc item similarities matrix
        nitems = len(data[0])
        self.data = data
        self.simmatrix = np.zeros((nitems,nitems))
        for i in xrange(nitems):
            for j in xrange(nitems):
                if j>=i:#triangular matrix
                   self.simmatrix[i,j] = sim(data[:,i],data[:,j])
                else:
                   self.simmatrix[i,j] = self.simmatrix[j,i]

    def GetKSimItemsperUser(self,r,K,u_vec):
        items = np.argsort(self.simmatrix[r])[::-1]
        items = items[items!=r]
        cnt=0
        neighitems = []
        for i in items:
            if u_vec[i]>0 and cnt<K:
               neighitems.append(i)
               cnt+=1
            elif cnt==K:
               break
        return neighitems
        
    def CalcRating(self,r,u_vec,neighitems):
        rating = 0.
        den = 0.
        for i in neighitems:
            rating +=  self.simmatrix[r,i]*u_vec[i]
            den += abs(self.simmatrix[r,i])
        if den>0:
            rating = np.round(rating/den,0)
        else:
            rating = np.round(self.data[:,r][self.data[:,r]>0].mean(),0)
        return rating
        
    def CalcRatings(self,u_vec,K,indxs=False):
        u_rec = copy.copy(u_vec)
        for r in xrange(len(u_vec)):
            if u_vec[r]==0:
               neighitems = self.GetKSimItemsperUser(r,K,u_vec)
               #calc predicted rating
               u_rec[r] = self.CalcRating(r,u_vec,neighitems)
        if indxs:
            #take out the rated movies
            seenindxs = [indx for indx in xrange(len(u_vec)) if u_vec[indx]>0]
            u_rec[seenindxs]=-1
            recsvec = np.argsort(u_rec)[::-1][np.argsort(u_rec)>0]
        
            return recsvec
        return u_rec
        
class LogLikelihood(object):
    def __init__(self,Umatrix,Movieslist,likethreshold=3):
        self.Movieslist = Movieslist
        #calculate loglikelihood ratio for each pair
        self.nusers = len(Umatrix)
        self.Umatrix =Umatrix
        self.likethreshold = likethreshold
        self.likerange = range(self.likethreshold+1,5+1)
        self.dislikerange = range(1,self.likethreshold+1)
        self.loglikelihood_ratio()

    def calc_k(self,a,b):
        tmpk = [[0 for j in range(2)] for i in range(2)]
        for ratings in self.Umatrix:
            if ratings[a] in self.likerange and ratings[b] in self.likerange:
               tmpk[0][0] += 1
            if ratings[a] in self.likerange and ratings[b] in self.dislikerange:
                tmpk[0][1] += 1
            if ratings[a] in self.dislikerange and ratings[b] in self.likerange:
                tmpk[1][0] += 1
            if ratings[a] in self.dislikerange and ratings[b] in self.dislikerange:
                tmpk[1][1] += 1
        return tmpk
        
    def calc_llr(self,k_matrix):
        Hcols=Hrows=Htot=0.0
        if sum(k_matrix[0])+sum(k_matrix[1])==0:
            return 0.
        invN = 1.0/(sum(k_matrix[0])+sum(k_matrix[1])) 
        for i in range(0,2):
            if((k_matrix[0][i]+k_matrix[1][i])!=0.0):
               Hcols += invN*(k_matrix[0][i]+k_matrix[1][i])*math.log((k_matrix[0][i]+k_matrix[1][i])*invN )#sum of rows
            if((k_matrix[i][0]+k_matrix[i][1])!=0.0):
               Hrows += invN*(k_matrix[i][0]+k_matrix[i][1])*math.log((k_matrix[i][0]+k_matrix[i][1])*invN )#sum of cols
            for j in range(0,2):
                if(k_matrix[i][j]!=0.0):
                   Htot +=invN*k_matrix[i][j]*math.log(invN*k_matrix[i][j])
        return 2.0*(Htot-Hcols-Hrows)/invN

    def loglikelihood_ratio(self):
        nitems = len(self.Movieslist)
        self.items_llr= pd.DataFrame(np.zeros((nitems,nitems))).astype(float)
        for i in xrange(nitems):
            for j in xrange(nitems):
                if(j>=i):
                   tmpk=self.calc_k(i,j)
                   self.items_llr.ix[i,j] = self.calc_llr(tmpk)
                else:
                   self.items_llr.ix[i,j] = self.items_llr.iat[j,i]
        print self.items_llr
        
    def GetRecItems(self,u_vec,indxs=False):
        items_weight = np.dot(u_vec,self.items_llr)
        sortedweight = np.argsort(items_weight)
        seenindxs = [indx for indx in xrange(len(u_vec)) if u_vec[indx]>0]
        seenmovies = np.array(self.Movieslist)[seenindxs]
        #remove seen items
        recitems = np.array(self.Movieslist)[sortedweight]
        recitems = [m for m in recitems if m not in seenmovies]
        if indxs:
            items_weight[seenindxs]=-1
            recsvec = np.argsort(items_weight)[::-1][np.argsort(items_weight)>0]
            return recsvec
        return recitems[::-1]