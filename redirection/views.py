from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from .models import *
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os
from company.models import Event

# Create your views here.
# @ratelimit(key='ip', rate='10/m')
def index(request):
    if 'email' and 'role' in request.session:
        email=request.session['email']
        role=request.session['role']
        
    # print(request.COOKIES.get('time'))
    events=Event.objects.filter()
    events_active = [event for event in events if not event.is_expired()]
    add=0
    event=[]
    for event1 in events_active:
        if add==7:
            break
        add+=1
        event.append(event1)
        

    # print(event)
    return render(request,'home.html',{'events':event})

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
        return render(request,'logs.html')
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