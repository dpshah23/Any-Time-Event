from django.shortcuts import render,redirect
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

# Create your views here.

@ratelimit(key='ip', rate='5/m')
def company_home(request):
    return HttpResponse("Welcome to Company Home Page")

# def 
@ratelimit(key='ip', rate='5/m')
def add_event(request):
    if request.session['role']!= "company" and 'email' not in request.session:
        return redirect('/')
    # if request.method == 'POST':
        # event_company = 

# def get_vol(request):
