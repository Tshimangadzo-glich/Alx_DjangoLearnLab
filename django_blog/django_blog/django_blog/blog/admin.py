from django.contrib import admin
from .models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'published_date', 'author']
    list_filter = ['published_date']
    search_fields = ['author']

admin.site.register(Post, PostAdmin)