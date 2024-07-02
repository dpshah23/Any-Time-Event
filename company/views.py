from django.shortcuts import render,redirect
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from auth1.models import company

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
        event_date = request.POST.get('date')
        event_time = request.POST.get('time')
        event_location = request.POST.get('location')
        event_loc_link = request.POST.get('location_link')
        event_description = request.POST.get('eventDescription')
        event_skills = request.POST.get('skills_needed')
        event_rep = request.POST.get('companyRep')
        event_rep_no = request.POST.get('contactNo')
        event_vol = request.POST.get('requiredVolunteers')
        event_mrp = request.POST.get('ratePerPerson')
        # event_completed =
        actual_amount = (event_mrp * 25)/100

# def get_vol(request):
