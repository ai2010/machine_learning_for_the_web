from django.db import models
from django.contrib.auth.models import User
import jsonfield
import json
import numpy as np

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    array = jsonfield.JSONField()
    arrayratedmoviesindxs = jsonfield.JSONField()
    name = models.CharField(max_length=1000)
    lastrecs = jsonfield.JSONField()

    def __unicode__(self):
            return self.name

    def save(self, *args, **kwargs):
        create = kwargs.pop('create', None)
        recsvec = kwargs.pop('recsvec', None)
        print 'create:',create
        if create==True:
            super(UserProfile, self).save(*args, **kwargs)
        elif recsvec!=None:
             self.lastrecs = json.dumps(recsvec.tolist())
             super(UserProfile, self).save(*args, **kwargs)
        else:
            nmovies = MovieData.objects.count()
            array = np.zeros(nmovies)
            ratedmovies = self.ratedmovies.all()
            self.arrayratedmoviesindxs = json.dumps([m.movieindx for m in ratedmovies])
            for m in ratedmovies:
                array[m.movieindx] = m.value
            self.array = json.dumps(array.tolist())
            super(UserProfile, self).save(*args, **kwargs)
    
class MovieRated(models.Model):
    user = models.ForeignKey(UserProfile, related_name='ratedmovies')
    movie = models.CharField(max_length=100)
    movieindx = models.IntegerField(default=-1)
    value = models.IntegerField()
    def __unicode__(self):
            return self.movie
            
class MovieData(models.Model):
    title = models.CharField(max_length=100)
    array = jsonfield.JSONField()
    ndim = models.IntegerField(default=300)
    description = models.TextField()