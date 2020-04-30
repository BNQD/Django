from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def homepage(request): #Any view - always pass request
    return HttpResponse("This is an <strong>awesome</strong> tutorial")
