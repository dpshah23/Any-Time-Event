from django.shortcuts import render,redirect
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit 
from django.contrib import messages
from company.models import *
from auth1.models import *

# Create your views here.
def volunteer_home(request):
    return HttpResponse("Welcome to Volunteer Home Page")

@ratelimit(key='ip', rate='5/m')
def apply (request,event_id):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    if request.session['role']== "company":
        messages.error(request,"You can not Apply to Events because this is a Company account ")
        return redirect('/')
    total_vol=RegVol.objects.filter(event_id_1=event_id)
    req = Event.objects.get(event_id=event_id).event_vol
    if len(total_vol) >= req :
        messages.error(request,"Maximum Limit of Volunteers has been reached...")
        return redirect('/')
    if request.session['role']== "volunteer":
            email = request.session['email']
   
            is_exists=RegVol.objects.get(email=email)
            if is_exists:
                messages.error(request,"You have already applied for this event")
                return redirect('/')
            
            email = request.session['email']
            company_email = Event.objects.get(event_id=event_id).company_email
            event_id_1 = event_id
            name = volunteer.objects.get(email=email).name
            email = email
            phone = volunteer.objects.get(email=email).phone
            skills = volunteer.objects.get(email=email).skills
            paid_status = False
            
            
            obj=RegVol(company_email=company_email,event_id_1=event_id_1,name=name , email=email ,phone=phone ,paid_status=paid_status) 
            obj.save()
            
            event_name=Event.objects.get(event_id=event_id_1).event_name
            messages.success(request,f"Applied Successfully to {event_name}")
            return redirect('/')
    
@ratelimit(key='ip', rate='10/m')
def applyerr(request):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    if request.session['role']== "company":
        messages.error(request,"You can not Apply to Events because this is a Company account ")
        return redirect('/')
    return render(request,"err_not_found.html")