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

# Create your views here.
@login_required(login_url='/dj-admin/')
def accept_user(request):
    vols=users.objects.filter(role="volunteer")
    vols_not = [users for users in vols if not users.is_expired()] 
    comp= users.objects.filter(role="company")
    final_vols=[]
    for email in vols_not.email:
        volobj=volunteer.objects.get(email=email)
        final_vols.append(volobj)
        
    context={'volunteers':final_vols,'companys':comp}
        
    
    
    return render(request, 'accept_user.html',context)

@login_required(login_url='/dj-admin/')
def pay(request):
    return render(request, 'pay.html')


@login_required(login_url='/dj-admin/')
def acceptyes(request,volemail):
    userchange=users.objects.get(email=volemail)
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
        volunteer.delete(email=volemail)
        users.delete(email=volemail)
        
    else:
        company.delete(email=volemail)
        users.delete(email=volemail)
        
    messages.error(request,"User Rejected")
    return redirect("/admincustom/acceptusers")
    