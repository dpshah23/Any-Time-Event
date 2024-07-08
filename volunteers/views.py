from django.shortcuts import render,redirect
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit 
from django.contrib import messages
from company.models import *
from auth1.models import *
from django.core.paginator import Paginator

# Create your views here.
@ratelimit(key='ip', rate='5/m')
def volunteer_home(request):
    return HttpResponse("Welcome to Volunteer Home Page")

@ratelimit(key='ip', rate='5/m')
def apply (request,event_id):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    
    try:
        event=Event.objects.get(event_id=event_id)
        if event.is_expired():
            messages.error(request,"Event has expired")
            return redirect('/')
    except Event.DoesNotExist:
        messages.error(request,"Event not found")
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
            try:
                existing_application = RegVol.objects.get(email=email, event_id_1=event_id)
                messages.error(request, "You have already applied for this event")
                return redirect('/')
            except RegVol.DoesNotExist:
                pass 

            email = request.session['email']
            company_email = Event.objects.get(event_id=event_id).company_email
            event_id_1 = event_id
            name = volunteer.objects.get(email=email).name
            email = email
            phone = volunteer.objects.get(email=email).phone
            skills = volunteer.objects.get(email=email).skills
            volid = volunteer.objects.get(email=email).vol_id
            paid_status = False
            
            
            obj=RegVol(company_email=company_email,event_id_1=event_id_1,name=name , email=email ,phone=phone ,paid_status=paid_status,vol_id=volid,skills=skills,attendence=False) 
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


@ratelimit(key='ip', rate="10/m")
def dispevents(request):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    if request.session['role']== "company":
        messages.error(request,"You can not Apply to Events because this is a Company account ")
        return redirect('/')
    
    email = request.session['email']

    # city=volunteer.objects.get(email=email).city
    # city=volunteer.objects.get(email=email).city
    city="ahmedabad"

    events=Event.objects.filter(event_city=city)

    events_expired = [event for event in events if event.is_expired()]  
    events_active = [event for event in events if not event.is_expired()]

    print(events_active,events_expired)
    
    page_number = request.GET.get('page_active',1)

    page_number1= request.GET.get('page_expired',1)

    paginator = Paginator(events_active, 9)
    paginator1 = Paginator(events_expired, 9)


    page_obj_active = paginator.get_page(page_number)
    page_obj_expired = paginator1.get_page(page_number1)

    print(page_obj_active,page_obj_expired)
    return render(request,"volunteer/events_disp.html",{'events_ex':page_obj_expired,'events':page_obj_active})

@ratelimit(key='ip',rate='10/m')
def profile(request,id):
    # print(id)
    # print('in profile')
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    
    if request.session['role']=="company":
        messages.error(request,"You Do Not have permission to view this page")
        return redirect('/')

    try:
        
        obj=volunteer.objects.get(vol_id=id)
        if obj.email!=request.session['email']:
            messages.error(request,"You Don't have permission to view this page")
        print(obj)
    except Exception as e:
        print("error")
        messages.error(request,"Volunteer Not Found")
        return redirect('/volunteer/')
    
    return render(request,"profile.html",{'obj':obj , 'is_volunteer': True})
    