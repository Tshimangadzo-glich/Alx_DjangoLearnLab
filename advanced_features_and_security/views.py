from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.shortcuts import remder, get_list_or_404, redirect
from .models import Book

#Create your views here.
from django.http import HttpResponse

permission_required("bookshelf.can_view_book", raise_exception=True)
def index(request):
    return HttpResponse("Welcome to my book shelf.")