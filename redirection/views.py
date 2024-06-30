from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from .models import *
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os

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

@login_required(login_url='/dj-admin/')
def logs(request):
    try:
        if not request.user.is_authenticated:
            return render(request,'err.html')
        else:
            if request.user.is_superuser:
                return render(request,'logs.html')
            else:
                return render(request,'err.html')
    except Exception as e:
        return HttpResponse(e)
    
@login_required(login_url='/login/')
def get_logs(request):
    log_file_path = 'logs/suspicious.log'  # Replace with the actual path to your log file
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as file:
            logs = file.readlines()
        return JsonResponse({'logs': logs})
    else:
        return JsonResponse({'error': 'Log file not found'}, status=404)