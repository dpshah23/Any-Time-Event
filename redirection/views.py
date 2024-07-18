from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from .models import *
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os
from company.models import Event
from django.utils import timezone  
from auth1.models import company
from .models import review
from company.models import RegVol
from datetime import date
from django.core.paginator import Paginator

# Create your views here.
'''

Function Name:
index

Description:
The index view function serves as the main landing page for a web application, displaying upcoming events, company logos associated with
these events, user reviews, and optionally, events a logged-in user has applied to. It also marks events as completed if their event date
has passed. If a user is logged in, it retrieves their email from the session and checks for events they have applied to (RegVol). 
It utilizes Django's timezone module to manage event dates and filtering.

Parameters:
request: The HTTP request object containing metadata about the request and user data.

Returns:
    -Renders the home.html template with context data:
    -events: Upcoming events sorted by event date.
    -logo: Logos associated with each event's organizing company.
    -applied_events: Events that the logged-in user has applied to (if authenticated).
    -reviews: All reviews available in the database.

Detailed Steps:
    Session Check: 
        Checks if 'email' and 'role' are present in the session. If not, assumes the user is not logged in.

    Update Event Completion: 
        Marks events as completed (event_completed=True) if their event date (event_date) is in the past (event_date__lt=now).

    Retrieve Events:    
        Fetches all events from the Event model and orders them by event_date.

    Filter Active Events: 
        Filters events to include only those that are not expired (events_active).

    Retrieve Company Logos: 
        Retrieves logos associated with each active event's organizing company (company_email) and limits to 7 events.

    Retrieve Reviews: 
        Retrieves all reviews (review objects) from the database.

    Authenticated User Handling: 
        If a user is authenticated (i.e., 'email' and 'role' are in the session):
        Retrieves the user's email from the session.
        Fetches events the user has applied to (applied_events) by querying RegVol for events associated with their email.
    
    Render Template: 
        Renders the home.html template with the gathered context data (events, logo, applied_events, reviews).

Usage: 
This function is central to displaying dynamic content on the application's homepage, catering to both logged-in and guest users. 
It leverages Django's ORM capabilities for efficient data retrieval and manipulation, ensuring that users are presented with relevant and
up-to-date information about events and their applications.
'''
@ratelimit(key='ip', rate='10/m')
def index(request):
    if 'email' and 'role' not in request.session:
        pass
        
    # print(request.COOKIES.get('time'))
    now=timezone.now().date()

    
    
    Event.objects.filter(event_date__lt=now, event_completed=False).update(event_completed=True)

    events=Event.objects.filter().order_by('event_date')
    events_active = [event for event in events if not event.is_expired()]
    add=0
    event=[]
    logos =[]
    for event1 in events_active:
        if add==7:
            break
        add+=1
        logo = company.objects.get(email=event1.company_email).logo
        event.append(event1)
        logos.append(logo)

    obj=review.objects.all().order_by('-date')[:3]

    if 'email' and 'role' in request.session:  
        email=request.session['email']
        applied_events = [regvol.event_id_1 for regvol in RegVol.objects.filter(email=email)]
        return render(request,'home.html',{'events':event,'logo':logos,'applied_events':applied_events,'reviews':obj})

    # print(event)
    # print(logos)


    
    return render(request,'home.html',{'events':event,'logo':logos,'reviews':obj})

@ratelimit(key='ip', rate='10/m')
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        
        obj1=contactus(name=name,email=email,message=message)
        obj1.save()
        
        messages.success(request,"Message sent successfully")
        return redirect('/')
        
        
        
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
    
def services(request):
    return render(request,'services.html')

def reviews(request):

    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        feedbackreview=request.POST.get('feedback')
        date1=date.today()

        print(name,email,feedbackreview,date1)

        objs=review(name=name,email=email,review=feedbackreview,date=date1)
        objs.save()

        messages.success(request,"Review Added Successfully")
        return redirect('/review')


    obj=review.objects.all().order_by('-date')

    page_number=request.GET.get('pg',1)

    paginator = Paginator(obj, 6)

    total_pages = paginator.num_pages

    print(total_pages)
    page_obj_active = paginator.get_page(page_number)

    return render(request,"reviews.html",{'reviews':page_obj_active,'total_pages':total_pages})

def privacy_policy(request):
    return render(request,'privacy.html')

def ourteam(request):
    return render(request,"Our_Team.html")

def termsandcond(request):
    return render(request,"Terms & Conditions.html")

def aboutus(request):
    return render(request,"About-Us.html")
