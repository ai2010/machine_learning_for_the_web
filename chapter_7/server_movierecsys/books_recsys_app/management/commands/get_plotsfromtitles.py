from django.core.management.base import BaseCommand
import os
import optparse
import numpy as np
import json
import pandas as pd
import requests

#python  manage.py get_plotsfromtitles --input=/Users/andrea/Desktop/book_packt/chapters_5/data/utilitymatrix.csv --outputplots=plots.csv --outputumatrix='umatrix.csv'
class Command(BaseCommand):
    '''
    option_list = BaseCommand.add_arguments() + (
            optparse.make_option('-i', '--input', dest='umatrixfile',
                                 type='string', action='store',
                                 help=('Input utility matrix')),   
            optparse.make_option('-o', '--outputplots', dest='plotsfile',
                                 type='string', action='store',
                                 help=('output file')),  
            optparse.make_option('--om', '--outputumatrix', dest='umatrixoutfile',
                                 type='string', action='store',
                                 help=('output file')),                             
        )
    '''
    
    def add_arguments(self, parser):

            parser.add_argument(
                '--input',
            action='store',
            help='Input utility matrix')
            
            parser.add_argument(
                '--outputplots', 
                 action='store',
                 help='output file')

            parser.add_argument(
                '--outputumatrix',
                 action='store',
                 help='output file')
        
    def getplotfromomdb(self,col,df_moviesplots,df_movies,df_utilitymatrix):
        string = col.split(';')[0]
        
        title=string[:-6].strip()
        year = string[-5:-1]      
        plot = ' '.join(title.split(' ')).encode('ascii','ignore')+'. '
        
        url = "http://www.omdbapi.com/?t="+title+"&y="+year+"&plot=full&r=json"
        
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"}
        r = requests.get(url,headers=headers)
        jsondata =  json.loads(r.content)
        if 'Plot' in jsondata:
            #store plot + title
            plot += jsondata['Plot'].encode('ascii','ignore')

        if plot!=None and plot!='' and plot!=np.nan and len(plot)>3:#at least 3 letters to consider the movie
            df_moviesplots.loc[len(df_moviesplots)]=[string,plot]
            df_utilitymatrix[col] = df_movies[col]
            print len(df_utilitymatrix.columns)

        return df_moviesplots,df_utilitymatrix
    
    def handle(self, *args, **options):
        print options
        pathutilitymatrix = options['input']
        df_movies = pd.read_csv(pathutilitymatrix)
        movieslist = list(df_movies.columns[1:])
        
        
        df_moviesplots = pd.DataFrame(columns=['title','plot'])
        df_utilitymatrix = pd.DataFrame()
        df_utilitymatrix['user'] = df_movies['user']
        
        print 'nmovies:',len(movieslist)
        for m in movieslist[:]:
            df_moviesplots,df_utilitymatrix=self.getplotfromomdb(m,df_moviesplots,df_movies,df_utilitymatrix)
            
        print len(df_movies.columns),'--',len(df_utilitymatrix.columns)
        outputfile = options['outputplots']
        df_moviesplots.to_csv(outputfile, index=False)
        outumatrixfile = options['outputumatrix']
        df_utilitymatrix.to_csv(outumatrixfile, index=False)
            