from django.contrib import admin
from django_markdown.admin import MarkdownField, AdminMarkdownWidget
from pages.models import SearchTerm,Page,Link

class SearchTermAdmin(admin.ModelAdmin):
    formfield_overrides = {MarkdownField: {'widget': AdminMarkdownWidget}}
    list_display = ['id', 'term', 'num_reviews']
    ordering = ['-id']
    
class PageAdmin(admin.ModelAdmin):
    formfield_overrides = {MarkdownField: {'widget': AdminMarkdownWidget}}
    list_display = ['id', 'searchterm', 'url','title','content']
    ordering = ['-id','-new_rank']
    
admin.site.register(SearchTerm,SearchTermAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(Link)