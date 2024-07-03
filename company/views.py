from django.shortcuts import render,redirect
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from auth1.models import company
from .models import *
import random , string
# Create your views here.

@ratelimit(key='ip', rate='5/m')
def company_home(request):
    return HttpResponse("Welcome to Company Home Page")

@ratelimit(key='ip', rate='5/m')
def add_event(request):
    if request.session['role']!= "company" and 'email' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        email = request.session('email')
        event_company = company.objects.get(email=email).name
        event_name = request.POST.get('eventName')
        alphanumeric_characters = string.ascii_letters + string.digits
        event_id = ''.join(random.choice(alphanumeric_characters) for _ in range(10))
        event_date = request.POST.get('date')
        event_time = request.POST.get('time')
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
        actual_amount = (event_mrp * 25)/100
        event1 = event(event_id=event_id,event_company=event_company,event_name=event_name,event_date=event_date,event_time=event_time,event_location=event_location,event_loc_link=event_loc_link,event_city=event_city,event_description=event_description,event_skills=event_skills,event_rep=event_rep,event_rep_no=event_rep_no,event_mrp=event_mrp,actual_amount=actual_amount)
        event1.save()

def getevent(request,event_id):
    event=event.objects.get(event_id=event_id)
    
    return render (request , "events.html",event=event)

    

# def get_vol(request):
