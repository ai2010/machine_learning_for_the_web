from django.contrib import admin
from books_recsys_app.models import MovieData,UserProfile

      
      
class MoviesAdmin(admin.ModelAdmin):
      list_display = ['title', 'description']

admin.site.register(UserProfile)
admin.site.register(MovieData,MoviesAdmin)
