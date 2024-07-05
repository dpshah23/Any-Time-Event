from django.shortcuts import render,redirect
from auth1.models import users,company,volunteer
from django.contrib import messages
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Create your views here.
def accept_user(request):
    return render(request, 'accept_user.html')

def pay(request):
    return render(request, 'pay.html')

def acceptyes(request,volemail):
    userchange=users.objects.get(email=volemail)
    userchange.is_active=True
    userchange.save()
    load_dotenv()
    from_email=os.getenv('EMAIL')
    password=os.getenv('PASSWORD1')

    print(from_email,password)

    subject="One Time Password For Login "
    length=8
    body=f"""

    <h1 style="text-align:center">One Time Password for Sign-in</h1>

    <p>
    Thank you for returning to our website. Since it has been over 15 days since your last login, we need to confirm your device.
    <br>
    To complete the login process, please use the following One-Time Password (OTP):
    </p>
    <p>
    Please enter this OTP on the login page to verify your identity and continue using your account.
    <br><br>
    If you did not request this login, please ignore this message.
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

    messages.error(request,"User Accepted")
    return redirect('admincustom/acceptusers')
    
    
def acceptno(request,volemail):
    userchange=users.objects.get(email=volemail)
    userchange.is_active=False
    userchange.save()

    load_dotenv()
    from_email=os.getenv('EMAIL')
    password=os.getenv('PASSWORD1')

    print(from_email,password)

    subject="One Time Password For Login "
    length=8
    body=f"""

    <h1 style="text-align:center">One Time Password for Sign-in</h1>

    <p>
    Thank you for returning to our website. Since it has been over 15 days since your last login, we need to confirm your device.
    <br>
    To complete the login process, please use the following One-Time Password (OTP):
    </p>
    <p>
    Please enter this OTP on the login page to verify your identity and continue using your account.
    <br><br>
    If you did not request this login, please ignore this message.
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
    