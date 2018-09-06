from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
#from django.template import RequestContext
from django.template import loader
from ast import literal_eval
import urllib
from books_recsys_app.models import MovieData,MovieRated,UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.conf import settings   
import logging
import json
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.core.cache import cache
import numpy as np
import unicodedata
import copy
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
tknzr = WordPunctTokenizer()
#nltk.download('stopwords')
stoplist = stopwords.words('english')
from nltk.stem.porter import PorterStemmer

umatrixpath = '/Users/andrea/Desktop/book_packt/chapters/7/server_movierecsys/umatrix.csv'
nmoviesperquery=5
nminimumrates=5
numrecs=5
recmethod = 'loglikelihood'


def PreprocessTfidf(texts,stoplist=[],stem=False):
    newtexts = []
    for text in texts:
        if stem:
           tmp = [w for w in tknzr.tokenize(text) if w not in stoplist]
        else:
           tmp = [stemmer.stem(w) for w in [w for w in tknzr.tokenize(text) if w not in stoplist]]
        newtexts.append(' '.join(tmp))
    return newtexts

def home(request):
    context={}
    if request.method == 'POST':
        post_data = request.POST
        data = {}
        data = post_data.get('data', None)
        if data:
            return redirect('%s?%s' % (reverse('books_recsys_app.views.home'),
                                urllib.urlencode({'q': data})))
    elif request.method == 'GET':
        get_data = request.GET
        data = get_data.get('q',None)
        titles = cache.get('titles')
        if titles==None:
            print 'load data...'
            texts = []
            mobjs = MovieData.objects.all()
            ndim = mobjs[0].ndim
            matr = np.empty([1,ndim])
            titles_list = []
            cnt=0
            for obj in mobjs[:]:
                texts.append(obj.description)
                newrow = np.array(obj.array)
                #print 'enw:',newrow
                if cnt==0:
                    matr[0]=newrow
                else:
                    matr = np.vstack([matr, newrow])
                titles_list.append(obj.title)
                cnt+=1
            vectorizer = TfidfVectorizer(min_df=1,max_features=ndim) 
            processedtexts = PreprocessTfidf(texts,stoplist,True)
            model = vectorizer.fit(processedtexts)
            cache.set('model',model)
            cache.set('data', matr)
            cache.set('titles', titles_list)
        else:
            print 'loaded',str(len(titles))
          
        Umatrix = cache.get('umatrix')
        if Umatrix.any()==None:
            df_umatrix = pd.read_csv(umatrixpath)
            Umatrix = df_umatrix.values[:,1:]
            print 'umatrix:',Umatrix.shape
            cache.set('umatrix',Umatrix)
            cf_itembased = CF_itembased(Umatrix)
            cache.set('cf_itembased',cf_itembased)
            cache.set('loglikelihood',LogLikelihood(Umatrix,movieslist))
            
        if not data:
            return render_to_response(
                'books_recsys_app/home.html',  context)
        
        
        #load all movies vectors/titles
        matr = cache.get('data')
        print 'matr',len(matr)
        titles = cache.get('titles')
        print 'ntitles:',len(titles)
        model_tfidf = cache.get('model')

        #load in cache rec sys methods
        print 'load methods...'
        

        #find movies similar to the query
        #print 'names:',len(model_tfidf.get_feature_names())
        queryvec = model_tfidf.transform([data.lower().encode('ascii','ignore')]).toarray()
        
        #print 'vec:', queryvec
        
        sims= cosine_similarity(queryvec,matr)[0]
        indxs_sims = list(sims.argsort()[::-1])
        #print indxs_sims
        titles_query = list(np.array(titles)[indxs_sims][:nmoviesperquery])
        
        context['movies']= zip(titles_query,indxs_sims[:nmoviesperquery])
        context['rates']=[1,2,3,4,5]
        return render_to_response(
            'books_recsys_app/query_results.html',  context)
        
def auth(request):
    print 'auth--:',request.user.is_authenticated()
    if request.method == 'GET':
        data = request.GET
        auth_method = data.get('auth_method')
        if auth_method=='sign in':
           return render_to_response(
               'books_recsys_app/signin.html',  {})
        else:    
            return render_to_response(
                'books_recsys_app/createuser.html', {})
    elif request.method == 'POST':
        post_data = request.POST
        name = post_data.get('name', None)
        pwd = post_data.get('pwd', None)
        pwd1 = post_data.get('pwd1', None)
        print 'auth:',request.user.is_authenticated()
        create = post_data.get('create', None)#hidden input
        if name and pwd and create:
           if User.objects.filter(username=name).exists() or pwd!=pwd1:
               return render_to_response(
                   'books_recsys_app/userexistsorproblem.html', request)
           user = User.objects.create_user(username=name,password=pwd)
           uprofile = UserProfile()
           uprofile.user = user
           uprofile.name = user.username
           uprofile.save(create=True)
           user = authenticate(username=name, password=pwd)
           login(request, user)
           return render_to_response(
               'books_recsys_app/home.html', request)
        elif name and pwd:
            user = authenticate(username=name, password=pwd)
            if user:
                login(request, user)
                return render_to_response(
                    'books_recsys_app/home.html', request)
            else:
                #notfound
                return render_to_response(
                    'books_recsys_app/nopersonfound.html', request)
                    
def signout(request):
    logout(request)
    return render_to_response(
        'books_recsys_app/home.html', request) 
        
def RemoveFromList(liststrings,string):
    outlist = []
    for s in liststrings:
        if s==string:
            continue
        outlist.append(s)
    return outlist
#since
def rate_movie(request):
    data = request.GET
    rate = data.get("vote")
    print request.user.is_authenticated()
    movies,moviesindxs = zip(*literal_eval(data.get("movies")))
    movie = data.get("movie")
    movieindx = int(data.get("movieindx"))
    #save movie rate
    userprofile = None
    if request.user.is_superuser:
        return render_to_response(
            'books_recsys_app/superusersignin.html', request)
    elif request.user.is_authenticated() :
        userprofile = UserProfile.objects.get(user=request.user)
    else:
        return render_to_response(
            'books_recsys_app/pleasesignin.html', request)
    
    if MovieRated.objects.filter(movie=movie).filter(user=userprofile).exists():
        mr = MovieRated.objects.get(movie=movie,user=userprofile)
        mr.value = int(rate)
        mr.save()
    else:
        mr = MovieRated()
        mr.user = userprofile
        mr.value = int(rate)
        mr.movie = movie
        mr.movieindx = movieindx
        mr.save()
        
    userprofile.save()
    #get back the remaining movies
    movies = RemoveFromList(movies,movie)
    moviesindxs = RemoveFromList(moviesindxs,movieindx)
    print movies
    context = {}
    context["movies"] = zip(movies,moviesindxs)
    context["rates"] = [1,2,3,4,5]
    return render_to_response(
        'books_recsys_app/query_results.html', context)
        
def movies_recs(request):
    
    userprofile = None
    print 'uuuu:',request.user.is_superuser
    if request.user.is_superuser:
        return render_to_response(
            'books_recsys_app/superusersignin.html',{})
    elif request.user.is_authenticated():
        userprofile = UserProfile.objects.get(user=request.user)
    else:
        return render_to_response(
            'books_recsys_app/pleasesignin.html', {})
    ratedmovies=userprofile.ratedmovies.all()
    print 'rated:',ratedmovies,'--',[r.movieindx for r in ratedmovies]
    context = {}
    if len(ratedmovies)<nminimumrates:
        context['nrates'] = len(ratedmovies)
        context['nminimumrates']=nminimumrates
        return render_to_response(
            'books_recsys_app/underminimum.html', context)
            
    u_vec = np.array(userprofile.array)
    #print 'uu:',u_vec
    Umatrix = cache.get('umatrix')
    #print Umatrix.shape,'--',len(u_vec)
    movieslist = cache.get('titles')
    #recommendation...
    u_rec = None
    if recmethod == 'cf_userbased':
        print recmethod
        u_rec = CF_userbased(u_vec,numrecs,Umatrix)
        
    elif recmethod == 'cf_itembased':
        print recmethod
        cf_itembased = cache.get('cf_itembased')
        if cf_itembased == None:
            cf_itembased = CF_itembased(Umatrix)
        u_rec = cf_itembased.CalcRatings(u_vec,numrecs)
        
    elif recmethod == 'loglikelihood':
        print recmethod
        llr = cache.get('loglikelihood')
        if llr == None:
            llr = LogLikelihood(Umatrix,movieslist)
        u_rec = llr.GetRecItems(u_vec,True)
        
    #save last recs
    userprofile.save(recsvec=u_rec)
    context['recs'] = list(np.array(movieslist)[list(u_rec)][:numrecs])
    return render_to_response(
        'books_recsys_app/recommendations.html', context)

from scipy.stats import pearsonr
from scipy.spatial.distance import cosine 
def sim(x,y,metric='cos'):
    if metric == 'cos':
       return 1.-cosine(x,y)
    else:#correlation
       return pearsonr(x,y)[0]
    
def CF_userbased(u_vec,K,data):
    def FindKNeighbours(r,data,K):
        neighs = []
        cnt=0
        for u in xrange(len(data)):
            if data[u,r]>0 and cnt<K:
               neighs.append(data[u])   
               cnt +=1 
            elif cnt==K:
               break
        return np.array(neighs)
        
    def CalcRating(u_vec,r,neighs):
        rating = 0.
        den = 0.
        for j in xrange(len(neighs)):
            rating += neighs[j][-1]*float(neighs[j][r]-neighs[j][neighs[j]>0][:-1].mean())
            den += abs(neighs[j][-1])
        if den>0:
            rating = np.round(u_vec[u_vec>0].mean()+(rating/den),0)
        else:
            rating = np.round(u_vec[u_vec>0].mean(),0)
        if rating>5:
            return 5.
        elif rating<1:
            return 1.
        return rating 
    #add similarity col
    data = data.astype(float)
    nrows = len(data)
    ncols = len(data[0])
    data_sim = np.zeros((nrows,ncols+1))
    data_sim[:,:-1] = data
    #calc similarities:
    for u in xrange(nrows):
        if np.array_equal(data_sim[u,:-1],u_vec)==False: #list(data_sim[u,:-1]) != list(u_vec):
           data_sim[u,ncols] = sim(data_sim[u,:-1],u_vec,'pearson')
        else:
           data_sim[u,ncols] = 0.
    #order by similarity:
    data_sim =data_sim[data_sim[:,ncols].argsort()][::-1]
    #find the K users for each item not rated:
    u_rec = copy.copy(u_vec)
    for r in xrange(ncols):
        if u_vec[r]==0:
           neighs = FindKNeighbours(r,data_sim,K)
           #calc the predicted rating
           u_rec[r] = CalcRating(u_vec,r,neighs)
    #take out the rated movies
    seenindxs = [indx for indx in xrange(len(u_vec)) if u_vec[indx]>0]
    u_rec[seenindxs]=-1
    recsvec = np.argsort(u_rec)[::-1][np.argsort(u_rec)>0]
    
    return recsvec
    
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
        
    def CalcRatings(self,u_vec,K):
        u_rec = copy.copy(u_vec)
        for r in xrange(len(u_vec)):
            if u_vec[r]==0:
               neighitems = self.GetKSimItemsperUser(r,K,u_vec)
               #calc predicted rating
               u_rec[r] = self.CalcRating(r,u_vec,neighitems)
        #take out the rated movies
        seenindxs = [indx for indx in xrange(len(u_vec)) if u_vec[indx]>0]
        u_rec[seenindxs]=-1
        recsvec = np.argsort(u_rec)[::-1][np.argsort(u_rec)>0]
        
        return recsvec
        
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