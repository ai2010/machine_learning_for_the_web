from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class SearchTerm(models.Model):
    term = models.CharField(_('search'), max_length=255)
    num_reviews = models.IntegerField(null=True,default=0)
    
    #display term on admin panel
    def __unicode__(self):
            return self.term

class Page(models.Model):
     searchterm = models.ForeignKey(SearchTerm, related_name='pages',null=True,blank=True)
     url = models.URLField(_('url'), default='', blank=True)
     title = models.CharField(_('name'), max_length=255)
     depth = models.IntegerField(null=True,default=-1)
     html = models.TextField(_('html'),blank=True, default='')
     review = models.BooleanField(default=False)
     old_rank = models.FloatField(null=True,default=0)
     new_rank = models.FloatField(null=True,default=1)
     content = models.TextField(_('content'),blank=True, default='')
     sentiment = models.IntegerField(null=True,default=100)
     
class Link(models.Model):
     searchterm = models.ForeignKey(SearchTerm, related_name='links',null=True,blank=True)
     from_id = models.IntegerField(null=True)
     to_id = models.IntegerField(null=True)