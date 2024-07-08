from django.shortcuts import render,redirect
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit
from auth1.models import company
from .models import *
import random , string
from django.contrib import messages
from datetime import timedelta
import razorpay
import os 
from dotenv import load_dotenv
from datetime import date
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
        event1 = Event(company_email = email , event_id=event_id,event_company=event_company,event_name=event_name,event_date=event_date,event_time=event_time,event_end_time=event_end_time,event_location=event_location,event_loc_link=event_loc_link,event_city=event_city.lower(),event_description=event_description,event_skills=event_skills,event_rep=event_rep,event_rep_no=event_rep_no,event_mrp=event_mrp,event_vol=event_vol,actual_amount=actual_amount)
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
    event1 = events.is_expired
    return render (request , "events.html",{'event':events , 'event1' : event1})

@ratelimit(key='ip', rate='5/m')
def getallevents(request):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    if request.session['role']== "volunteer":
        messages.error(request,"You are not authorized to view this page")
        return redirect('/')
    
    email=request.session['email']
    all_events = Event.objects.filter(company_email=email)
    events_expired = [event for event in all_events if event.is_expired()]  
    events_active = [event for event in all_events if not event.is_expired()]
    
    return render(request,"all_events.html",{'events_ex':events_expired,'events':events_active,'company_name':company.objects.get(email=email).name , 'obj' : company.objects.get (email = email)})


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



@ratelimit(key='ip',rate='10/m')
def profile(request,id):
    # print(id)
    # print('in profile')
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    
    if request.session['role']=="volunteer":
        messages.error(request,"You Don't have permission to view this page")

    try:
        
        obj=company.objects.get(comp_id=id)
        if obj.email!=request.session['email']:
            messages.error(request,"You Don't have permission to view this page")
        print(obj)
    except Exception as e:
        print("error")
        messages.error(request,"Company Not Found")
        return redirect('/company/')
    
    return render(request,"profile.html",{'data':obj , 'is_company': True})
    

@ratelimit(key='ip',rate='5/m')
def getpayment (request , event_id):
    load_dotenv()
    key = os.getenv('api_key_razorpay')
    secret = os.getenv('api_secret_razorpay')
    client = razorpay.Client(auth=(key,secret))
    
    total_vol=len(RegVol.objects.filter(event_id_1=event_id,attendence=True))
    amount = (Event.objects.get(event_id=event_id).event_mrp) * total_vol
    final_amt = int(amount)*100
    payment = client.order.create({ "amount": final_amt, "currency": "INR", "payment_capture": '1' })
    # print(payment)
    # company_success.payment_id = payment['id']
    # company_success.save()
    timestamp = date.today()
    payment_id = payment['id']
    pay = company_success(timestamp=timestamp , payment_id = payment_id)
    pay.save()
    event, created = Event.objects.update_or_create(
    event_id=event_id,
    defaults={'paid_status': True}
)

    return render (request ,"payment.html" , {'payment':payment})

def editevent(request,event_id1):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    
    if request.session['role']=="volunteer":
        messages.error(request,"You Don't have permission to view this page")
    try:

        event=Event.objects.get(event_id=event_id1)

        if request.method=="POST":
            email = request.session['email']
            event_company = company.objects.get(email=email).name
            event_name = request.POST.get('eventName')
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
            actual_amount = int(event_mrp) - ((int(event_mrp) * 25)/100)
            obj, created = Event.objects.update_or_create(
                event_id=event_id1,
                defaults={
                    'event_name':event_name,
                    'event_date':event_date,
                    'event_time':event_time,
                    'event_end_time':event_end_time,
                    'event_location':event_location,
                    'event_loc_link':event_loc_link,
                    'event_city':event_city.lower(),
                    'event_description':event_description,
                    'event_skills':event_skills,
                    'event_rep':event_rep,
                    'event_rep_no':event_rep_no,
                    'event_mrp':event_mrp,
                    'event_vol':event_vol,
                    'actual_amount':actual_amount,
                }
            )
            

            print("Updated")
            messages.success(request,'Event Details Updated Successfully')
            return redirect('/company/events/')
    except Event.DoesNotExist:
        messages.error('Event Does Not Exists')
        return redirect('/company/')
    except Exception as e:
        print(e)
        return redirect('/')

    return render(request,'edit_event.html',{'event':event})

def markattendenceyes(request,event_id,email):
    obj=RegVol.objects.get(event_id_1=event_id,email=email)
    obj.attendence=True
    obj.save()
    messages.success(request,"Attendence Marked To Present")
    return redirect(f'/company/get_volunteers/{event_id}')


def markattendenceno(request,event_id,email):
    obj=RegVol.objects.get(event_id_1=event_id,email=email)
    obj.attendence=False
    obj.save()
    messages.success(request,"Attendence Marked To Absent")
    return redirect(f'/company/get_volunteers/{event_id}')


