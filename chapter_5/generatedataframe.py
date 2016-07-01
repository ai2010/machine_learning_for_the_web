import numpy as np
import pandas as pd
import collections
#data
df = pd.read_csv('./data/ml-100k/u.data',sep='\t',header=None)
#movie list
df_info = pd.read_csv('./data/ml-100k/u.item',sep='|',header=None)
movielist = [df_info[1].tolist()[indx]+';'+str(indx+1) for indx in xrange(len(df_info[1].tolist()))]
nmovies = len(movielist)
nusers = len(df[0].drop_duplicates().tolist())  

min_ratings = 50
movies_rated  = list(df[1]) 
counts = collections.Counter(movies_rated)
print counts
print 'ratings less than ',min_ratings,':',len(collections.Counter(el for el in counts.elements() if counts[el] <min_ratings))
dfout = pd.DataFrame(columns=['user']+movielist)

toremovelist = []
for i in range(1,nusers):
    tmpmovielist = [0 for j in range(nmovies)]
    dftmp =df[df[0]==i]
    for k in dftmp.index:
        #print dftmp.ix[k].tolist(),'-',dftmp.ix[k][1]
        if counts[dftmp.ix[k][1]]>= min_ratings:           
           tmpmovielist[dftmp.ix[k][1]-1] = dftmp.ix[k][2]
           
        else:
           toremovelist.append(dftmp.ix[k][1])
            
    dfout.loc[i] = [i]+tmpmovielist
  
toremovelist = list(set(toremovelist))
dfout.drop(dfout.columns[toremovelist], axis=1, inplace=True)
print dfout.head()
dfout.to_csv('data/utilitymatrix.csv',index=None)

#matrix movies's content
movieslist = [int(m.split(';')[-1]) for m in dfout.columns[1:]]
moviescats = ['unknown','Action','Adventure','Animation','Children\'s','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western']
dfout_movies =  pd.DataFrame(columns=['movie_id']+moviescats)
startcatsindx = 5
cnt= 0
for m in movieslist:
    dfout_movies.loc[cnt] = [m]+df_info.iloc[m-1][startcatsindx:].tolist()
    cnt +=1 
print dfout_movies.head()

dfout_movies.to_csv('data/movies_content.csv',index=None)
#remove empty columns
cntremoved = 0
ncols = len(dfout.columns)
cols = dfout.columns
removed_list = []
for col in xrange(1,ncols):
    check = np.array(dfout[cols[col]]).sum()    
    if check<1.:
        removed_list.append(col)
        print 'remove:',cols[col],' c:',counts[col]
        cntremoved +=1

print 'aa',len(toremovelist)
print '0cls:',cntremoved,'--',len(dfout.columns),'--',ncols-cntremoved

for c in dfout.columns:
    if np.array(dfout[c]).sum() ==0.:
        print 'wrong:',c