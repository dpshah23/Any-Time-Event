from django.shortcuts import render,redirect
from auth1.models import users,company,volunteer
from django.contrib import messages
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from django.contrib.auth.decorators import login_required
from datetime import date , timedelta
from django.utils import timezone
from company.models import Event,RegVol
from django.conf import settings

# Create your views here.
def accept_user(request):
    # Fetch volunteers who are not expired
    vols = users.objects.filter(role="volunteer").filter(is_active=True)
    
    # Fetch companies
    comps = users.objects.filter(role="company")
    
    final_vols = []
    final_comps = []


    for comp in comps:
        try:
            compobj = company.objects.get(email=comp.email)
            
            final_comps.append( compobj)
        except company.DoesNotExist:
            pass
    
    # Retrieve volunteer objects based on their email and prepare for context
    for user in vols:
        try:
            volobj = volunteer.objects.get(email=user.email)

            final_vols.append( volobj )


        except volunteer.DoesNotExist:
            pass  # Handle case where volunteer object does not exist
    
    print(final_vols)
    print(final_comps)

    
    context = {
        'volunteers': final_vols,
        'companys': final_comps
    }
    
    return render(request, 'accept_vol.html', context)

@login_required(login_url='/dj-admin/')
def pay(request):

    rem_payment=Event.objects.filter()
    print(rem_payment)
    return render(request, 'event_payment.html',{'events_ex':rem_payment})


@login_required(login_url='/dj-admin/')
def acceptyes(request,volemail):
    try:
        userchange=users.objects.get(email=volemail)
    except Exception as e:
        pass
    userchange.is_active=True
    userchange.save()
    load_dotenv()
    from_email=os.getenv('EMAIL')
    password=os.getenv('PASSWORD1')

    print(from_email,password)

    subject="You are now an Authorized user"
    length=8
    body=f"""

    <h1 style="text-align:center">Authorization done</h1>

    <p>
    Thank you for registering to our website. 
    <br>
    You can now login to our site with your credentials . 
    <br>
    </p>
    <p>
    Please enter this OTP after the login page which we share to verify your identity and continue using your account.
    <br><br>
   
    </p>

    <p>Thank you,<br>
    Any Time Event Team</p>

    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = volemail
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, volemail, msg.as_string())

    messages.error(request,"User Accepted")
    return redirect('admincustom/accept_vol')
    
@login_required(login_url='/dj-admin/')    
def acceptno(request,volemail):
    userchange=users.objects.get(email=volemail)
    userchange.is_active=False
    userchange.save()
    print(volemail)

    load_dotenv()
    from_email=os.getenv('EMAIL')
    password=os.getenv('PASSWORD1')

    print(from_email,password)

    subject="Authorization Failed"
    length=8
    body=f"""

    <h1 style="text-align:center">Failed Attemp</h1>

    <p>
    Thank you for registering to our website. But we are really sorry to inform you that you can not be a part of our website
    <br>
    we found some details which are not appropriate so please try again .
    <br>
    </p>
    <p> Thank You for giving us your time 
    </p>

    <p>Thank you,<br>Any Time Event Team</p>

    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = volemail
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, volemail, msg.as_string())
    
    if userchange.role=="volunteer":
        volunteer.objects.filter(email=volemail).delete()
        users.objects.filter(email=volemail).delete()        
    else:
        company.objects.filter(email=volemail).delete()
        users.objects.filter(email=volemail).delete()
        
    messages.error(request,"User Rejected")
    return redirect("/admincustom/acceptusers")
    