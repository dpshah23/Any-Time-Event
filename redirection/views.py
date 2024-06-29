from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
from django_ratelimit.decorators import ratelimit

# Create your views here.
@ratelimit(key='ip', rate='10/m')
def index(request):
    if 'email' and 'role' in request.session:
        email=request.session['email']
        role=request.session['role']
        if role=="volunteer":
                       
            return HttpResponse("Volunteer")
        elif role=="company":
            return HttpResponse("Company")
        else:
            redirect('/')
    return render(request,'home.html')

@ratelimit(key='ip', rate='10/m')
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        
        obj1=contactus(name=name,email=email,message=message)
        obj1.save()
        
        messages.success(request,"Message sent successfully")
        
        
        
    return render(request,'Contact-us.html')