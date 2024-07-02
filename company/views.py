from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.

def company_home(request):
    return HttpResponse("Welcome to Company Home Page")

# def 
def add_event(request):
    if request.session['role']!= "company" and 'email' not in request.session:
        return redirect('/')
    # if request.method == 'POST':
        # event_company = 

# def get_vol(request):
