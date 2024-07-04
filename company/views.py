from django.shortcuts import render,redirect
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from auth1.models import company
from .models import *
import random , string
from django.contrib import messages
from datetime import timedelta
# Create your views here.

@ratelimit(key='ip', rate='5/m')
def company_home(request):
    return HttpResponse("Welcome to Company Home Page")

@ratelimit(key='ip', rate='5/m')
def add_event(request):
    # print(request.session['role'])
    # print(request.session['email'])
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    if request.session['role']== "volunteer":
        messages.error(request,"You are not authorized to view this page")
        return redirect('/')
    if request.method == 'POST':
        email = request.session['email']
        event_company = company.objects.get(email=email).name
        event_name = request.POST.get('eventName')
        alphanumeric_characters = string.ascii_letters + string.digits
        event_id = ''.join(random.choice(alphanumeric_characters) for _ in range(10))
        event_date = request.POST.get('date')
        event_time = request.POST.get('time')
        event_end_time = request.POST.get('etime')
        event_location = request.POST.get('location')
        event_loc_link = request.POST.get('location_link')
        event_city = request.POST.get('event_city')
        event_description = request.POST.get('eventDescription')
        event_skills = request.POST.get('skills_needed')
        event_rep = request.POST.get('companyRep')
        event_rep_no = request.POST.get('contactNo')
        event_vol = request.POST.get('requiredVolunteers')
        event_mrp = request.POST.get('ratePerPerson')
        # event_completed =
        actual_amount = int(event_mrp) - ((int(event_mrp) * 25)/100)
        print(actual_amount)
        event1 = Event(company_email = email , event_id=event_id,event_company=event_company,event_name=event_name,event_date=event_date,event_time=event_time,event_end_time=event_end_time,event_location=event_location,event_loc_link=event_loc_link,event_city=event_city,event_description=event_description,event_skills=event_skills,event_rep=event_rep,event_rep_no=event_rep_no,event_mrp=event_mrp,event_vol=event_vol,actual_amount=actual_amount)
        event1.save()
        
        messages.success(request,"Event Added Successfully")
        return redirect('/company/')
        
    return render(request,"add_events.html")

@ratelimit(key='ip', rate='5/m')
def getevent(request,event_id):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    if request.session['role']== "volunteer":   
        messages.error(request,"You are not authorized to view this page")
        return redirect('/')
    try:
        email=request.session['email']
        events=Event.objects.get(event_id=event_id,company_email=email)
        # num_vol = reg_vol.objects.get(event_id=event_id)
        # print(num_vol)
    except Event.DoesNotExist:
        messages.error(request,"Event Not Found")
        return redirect('/company/')
    
    return render (request , "events.html",{'event':events})

@ratelimit(key='ip', rate='5/m')
def getallevents(request):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    if request.session['role']== "volunteer":
        messages.error(request,"You are not authorized to view this page")
        return redirect('/')
    
    email=request.session['email']
    all_events = Event.objects.filter(company_email=email,)
    events_expired = [event for event in all_events if event.is_expired()]  
    events_active = [event for event in all_events if not event.is_expired()]
    return render(request,"all_events.html",{'events_ex':events_expired,'events':events_active,'company_name':company.objects.get(email=email).name})


@ratelimit(key='ip', rate='10/m')
def gettotalvol(request,event_id):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    if request.session['role']== "volunteer":
        messages.error(request,"You are not authorized to view this page")
        return redirect('/')
    email=request.session['email']
    # events = Event.objects.filter(company_email=email,event_id=event_id)
    try:
        events = Event.objects.get(company_email=email,event_id=event_id)
        volunteers = RegVol.objects.filter(event_id_1=event_id)

        return render(request,"list_of_attendes.html",{'event':events,'volunteers':volunteers,'length':len(volunteers)})

    except Event.DoesNotExist:
        messages.error(request,"Event Not Found")
        return redirect('/company/')
    except RegVol.DoesNotExist:
        messages.error(request,"No Volunteers Registered")
        return redirect('/company/')
    


    

# def get_vol(request):

