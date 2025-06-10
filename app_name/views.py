from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Home Page</h1>")

def blist(request):
    return HttpResponse("<h1>Blist Page</h1>")