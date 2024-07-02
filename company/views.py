from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def company_home(request):
    return HttpResponse("Welcome to Company Home Page")