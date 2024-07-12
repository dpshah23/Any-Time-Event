from django.shortcuts import render,redirect
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit 
from django.contrib import messages
from company.models import *
from auth1.models import *
from CustomAdmin.models import payout
from django.core.paginator import Paginator
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import os
import base64
from dotenv import load_dotenv
from datetime import datetime


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
    
    comp_mail=Event.objects.get(event_id=event_id).company_email
    event_name=Event.objects.get(event_id=event_id).event_name
    event_date=Event.objects.get(event_id=event_id).event_date
    event_company=Event.objects.get(event_id=event_id).event_company
    event_time=Event.objects.get(event_id=event_id).event_time
    event_end_time=Event.objects.get(event_id=event_id).event_end_time
    event_location=Event.objects.get(event_id=event_id).event_location
    length=req
    print(length)
    print(len(total_vol))
    

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
            event_date=Event.objects.get(event_id=event_id_1).event_date
            event_time=Event.objects.get(event_id=event_id_1).event_time.strftime("%I:%M %p")
            event_end_time=Event.objects.get(event_id=event_id_1).event_end_time.strftime("%I:%M %p")
            event_location=Event.objects.get(event_id=event_id_1).event_location
            event_company=Event.objects.get(event_id=event_id_1).event_company
            event_loc_link=Event.objects.get(event_id=event_id_1).event_loc_link

            smtp_server = 'smtp.gmail.com'
            port = 587

            subject = f"Application Received for {event_name}"
            body = f"""
            <h1 style="text-align:center">Application Received</h1>
            <p>
            Dear Volunteer,
            </p>
            <p>
            We are pleased to inform you that your application for the event "{event_name}" has been received successfully.
            </p>
            <p>
            <strong>Event Details:</strong><br>
            Date: {event_date}<br>
            Time: {event_time}<br>
            End Time: {event_end_time}<br>
            Location: {event_location}<br>
            Organized by: {event_company}<br>
            Location Link: {event_loc_link}<br>
            </p>
            <p>
            Thank you for your interest in participating. We will review your application and contact you with further details soon.
            </p>
            <p>
                If you have any questions or need further assistance, please do not hesitate to contact us.
            </p>
            <p>Best regards,<br>Any Time Event Team</p>
        """
    load_dotenv()
    from_email=os.getenv('EMAIL')
    password=os.getenv('PASSWORD1')
    sendmail(smtp_server, port, from_email, password, subject, body,email, event_name, event_date, event_time, event_location ,event_end_time)


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
    city=volunteer.objects.get(email=email).city
    # city="ahmedabad"

    events=Event.objects.filter(event_city=city)

    events_expired = [event for event in events if event.is_expired()]  
    events_active = [event for event in events if not event.is_expired()]

    print(events_active,events_expired)

    applied_events = [regvol.event_id_1 for regvol in RegVol.objects.filter(email=email)]

    return render(request, "volunteer/events_disp.html", {
        'events_ex': events_expired,
        'events': events_active,
        'applied_events': applied_events
    })

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
        email = volunteer.objects.get(vol_id = id ).email
        obj=volunteer.objects.get(vol_id=id)
        if obj.email!=request.session['email']:
            messages.error(request,"You Don't have permission to view this page")
        print(obj)
    except Exception as e:
        print("error")
        messages.error(request,"Volunteer Not Found")
        return redirect('/volunteer/')
    
    return render(request,"profile.html",{'obj':obj , 'is_volunteer': True , 'volunteer':email})
    
def getevent(request,id):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    
    if request.session['role']=="company":
        messages.error(request,"You Do Not have permission to view this page")
        return redirect('/')

    try:
        event=Event.objects.get(event_id=id)
        try:
            email=request.session['email']
            isreg=RegVol.objects.get(event_id_1=id,email=email)
            unregistered=True
        except RegVol.DoesNotExist:
            unregistered=False

            pass
    except Event.DoesNotExist:
        messages.error(request,'Event Does Not Exist')
        return redirect('/volunteer/events/')
    

    return render(request,"volunteer/events.html",{'event':event,'unregistered':unregistered})


def unregister(request,event_id):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    
    if request.session['role']=="company":
        messages.error(request,"You Do Not have permission to view this page")
        return redirect('/')

    try:
        email=request.session['email']
        isreg=RegVol.objects.get(email=email,event_id_1=event_id)
        isreg.delete()

        messages.success(request,"UnRegistered From Event Successfully")

        return redirect('/volunteer/events/')

    except RegVol.DoesNotExist:
        messages.error(request,"You Didn't apply in this event")
        return redirect('/volunteer/events/')
    
def sendmail(smtp_server, port, sender_email, sender_password, subject, body,recipient, event_name, event_date, event_time, event_location ,event_end_time):
    cal = generate_ics(event_name, event_date, event_time, event_location,event_end_time)
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  
    server.login(sender_email, sender_password)
   
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

      
    msg.attach(MIMEText(body, 'html'))

    part = MIMEBase('text', 'calendar')
    part.set_payload(cal)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{event_name}.ics"')
    msg.attach(part)

    server.sendmail(sender_email, recipient, msg.as_string())
    print(f"Email sent to {recipient}")


    server.quit()

def generate_ics(event_name, event_date, event_time, event_location,event_end_time):
    event_begin = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %I:%M %p")
    event_end = datetime.strptime(f"{event_date} {event_end_time}", "%Y-%m-%d %I:%M %p")
    
    cal = f"""BEGIN:VCALENDAR
    VERSION:2.0
    PRODID:-//hacksw/handcal//NONSGML v1.0//EN
    BEGIN:VEVENT
    SUMMARY:{event_name}
    DTSTART:{event_begin.strftime('%Y%m%dT%H%M%S')}
    DTEND:{event_end.strftime('%Y%m%dT%H%M%S')}
    LOCATION:{event_location}
    END:VEVENT
    END:VCALENDAR
    """
    return cal

def editvol(request,vol_id):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')

    if request.session['role']=="company":
        messages.error(request,"You Don't have permission to view this page")
    try:

        

        vol = volunteer.objects.get(vol_id=vol_id)
        if request.method=="POST":

            if 'profile_picture' in request.FILES:
                image_file = request.FILES['profile_picture']
                valid_extensions = ['jpg', 'png', 'jpeg', 'heic']
                if image_file.name.split('.')[-1].lower() not in valid_extensions:
                    messages.error(request, 'Invalid Image format. Only JPG, PNG, JPEG, and HEIC are allowed.')
                    return render(request, 'edit_vol.html', {'volunteer': vol})

                image_data = image_file.read()
                profile_pic = base64.b64encode(image_data).decode('utf-8')
            else:
                profile_pic = vol.profile_pic 
        
            email = request.session['email']
            id = volunteer.objects.get(email= email).vol_id
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            dob = request.POST.get('dob')
            experience = request.POST.get('experience')
            skills = request.POST.get('skills')
            qualification = request.POST.get('qualification')
            emergency_contact = request.POST.get('emergency_contact')
            city = request.POST.get('city')
            # description = request.POST.get('description')
            obj, created = volunteer.objects.update_or_create(
                email=email,
                defaults={
                    'name':name,
                    'phone' :phone,
                    'dob': dob,
                    'experience' : experience,
                    'skills' : skills,
                    'qualification' : qualification,
                    'emergency_contact' : emergency_contact,
                    'city' : city,
                    'profile_pic':profile_pic
                    
                }
            )
            

            print("Updated")
            messages.success(request,'Volunteer Details Updated Successfully')
            return redirect(f'/volunteer/profile/{id}')
    except volunteer.DoesNotExist:
        messages.error(request,'volunteer Does Not Exists')
        return redirect('/volunteer/')
    except Exception as e:
        print(e)
        return redirect('/')

    return render(request,'edit_vol.html',{'volunteer':vol})

@ratelimit(key='ip',rate='5/m')
def history(request):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')

    if request.session['role']=="company":
        messages.error(request,"You Don't have permission to view this page")
        return redirect('/')
    
    email = request.session['email']
    try:
        vol_id = volunteer.objects.get(email = email).vol_id
        history = payout.objects.filter(vol_id=vol_id)
        
    except volunteer.DoesNotExist:
        messages.error(request,'volunteer Does Not Exists')
        return redirect('/')
    except Exception as e:
        print(e)
    return render(request ,'transaction.html' , {'history' : history} )