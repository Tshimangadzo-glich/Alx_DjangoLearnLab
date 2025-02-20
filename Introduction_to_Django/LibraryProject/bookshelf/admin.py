from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','publication_year')
    list_filter = ('pubilcation_year',)
    search_fields = ('title','author')
    register
