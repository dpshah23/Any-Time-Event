from django.shortcuts import render,redirect,HttpResponse
from .models import users,otps
from cryptography.fernet import Fernet
import base64
from django.contrib import messages
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import random
import os


# Create your views here.

def validate(request):
    if request.method=="POST":
        otp=request.POST.get('otp')
        email=request.COOKIES.get('email')
        user=otps.objects.get(email=email)
        if user.otp==int(otp):
            user.usage=True
            user.save()
            request.session['email']=email
            request.session['role']=users.objects.get(email=email).role
            if users.objects.get(email=email).role=="volunteer":
                user.delete()
                return redirect('/volunteer')
            elif users.objects.get(email=email).role=="company":
                user.delete()
                return redirect('/company')
            else:
                user.delete()
                return redirect('/')
        else:
            messages.error(request, 'Invalid OTP')
            return render(request, 'validate.html')
        

    return render(request, 'validate.html')

def decrypt_password(password,key):
    decoded_key = base64.b64decode(key)
    decoded_password = base64.b64decode(password)

    f = Fernet(decoded_key)
   
    decrypted_password = f.decrypt(decoded_password)
    
    return decrypted_password.decode()


def login(request):
    if 'email' and 'role' in request.session:
        pass
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=users.objects.all(email=email)
            decrypted_pass=decrypt_password(user.password,user.key)
            if user.email==email and decrypted_pass==password:
                if request.COOKIES.get('time'):
                    load_dotenv()
                    from_email=os.getenv('EMAIL')
                    password=os.getenv('PASSWORD')

                    subject="One Time Password For Admin "
                    length=8
                    otp=random.randint(000000,999999)
                    body=f"""

                    <h1 style="text-align:center">One Time Password For Sign-in</h1>

                    <p>Thank you for registering on our website again but you need to confirm your device because it has been over 15 days since you last logged in .<br>
                    To complete the registration process, please use the following One-Time Password (OTP) </p>

                    <h2>Your OTP : {otp}</h2>

                    <p>
                    Please enter this OTP on the registration page to verify your identity and activate your account.

                    If you did not initiate this registration, please ignore this message.
                
                    </p>

                    Thank you,
                    <br>
                    Any Time Event.

                    """
                    msg = MIMEMultipart()
                    msg['Subject'] = subject
                    msg['From'] = from_email
                    msg['To'] = email
                    msg.attach(MIMEText(body, 'html'))
                    user1=otps(email=email,otp=otp,usage=False)
                    user1.save()
                    response = HttpResponse('')
                    response.set_cookie('email', email)


                    with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()
                        server.login(from_email, password)
                        server.sendmail(from_email, email, msg.as_string())
                        print("OTP Send Successfully")
                        
                        
                        return redirect('/validate')
                else:
                    if user.role=="volunteer":
                        # return redirect('/volunteer')
                        return HttpResponse("Volunteer")
                    elif user.role=="company":
                        return HttpResponse("Company")
                    else:
                        redirect('/')

                

        except:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'Log-In.html')

    return render(request, 'Log-In.html')



def logout(request):
    del request.session['email']
    del request.session['role']
    return redirect('/')