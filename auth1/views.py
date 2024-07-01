from django.shortcuts import render,redirect,HttpResponse
from .models import *
from cryptography.fernet import Fernet
import base64
from django.contrib import messages
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import random,string
import os
from django_ratelimit.decorators import ratelimit
from datetime import date
from datetime import timedelta


# Create your views here.

@ratelimit(key='ip', rate='10/m')
def validate(request):
    if request.method=="POST":
        otp=request.POST.get('otp')
        email=request.COOKIES.get('email')
        user=otps.objects.get(email=email)
        if user.otp==int(otp) and not user.is_expired():   
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

@ratelimit(key='ip', rate='10/m')
def login(request):
    if 'email' and 'role' in request.session:
        return redirect('/')
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
                    expiry_duration = timedelta(minutes=5)  # Set OTP validity duration
                    expires_at = timezone.now() + expiry_duration
                    user1=otps(email=email,otp=otp, expires_at=expires_at)
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

            else:
                messages.error(request, 'Invalid Credentials')
                return render(request, 'Log-In.html')

        except:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'Log-In.html')

    return render(request, 'Log-In.html')

def key():
    
    return Fernet.generate_key()


@ratelimit(key='ip', rate='10/m')
def signup (request):
    if request.method == 'POST':
        if users.objects.all (email!=email) :

            email = request.POST.get('email')

            if users.objects.filter(email=email).exists():
                messages.error(request, 'Email Already Exist')
                return render(request, 'Sign-Up.html')
        
            password = request.POST.get('password')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            role = request.POST.get('role')
            
            key1=key()
            f=Fernet(key1)
            encrypt=f.encrypt(password.encode())
            encrypted_password = base64.b64encode(encrypt).decode('utf-8')
            key_str = base64.b64encode(key1).decode('utf-8')

         
            response = HttpResponse("Cookie Set")
            response.set_cookie('email', email, max_age=3600) 
            response = HttpResponse("Cookie Set")
            response.set_cookie('name', name, max_age=3600) 
            response = HttpResponse("Cookie Set")
            response.set_cookie('phone', phone, max_age=3600) 
        
            user1 = users(email=email,password=encrypted_password,key=key_str,role=role)
            user1.save()
            
            if role == "company":
                c1=company(name=name,email=email,phone1=phone,address=None,website=None , phone2=None ,card=None , description=None , logo=None )
                c1.save()
                return redirect('/companyinfo')
            else :
                v1 = volunteer(name=name ,email=email,phone=phone ,dob=None , timestamp=None ,experience=None , skills=None , qualification=None , upi=None,emergency_contact=None,profile_pic=None,card=None,description=None )
                v1.save()
                return redirect('/volunteerinfo')
       
        else : 
            messages.error(request, 'Email Already Exist')
            return render(request, 'Sign-Up.html')
        return redirect('/')
    return render(request, 'Sign-Up.html')

@ratelimit(key='ip', rate='10/m')
def companyinfo(request):
    if request.method == 'POST':
        email1 = request.COOKIES.get('email')
        name = request.COOKIES.get('name')
        phone = request.COOKIES.get('phone')
        address = request.POST.get('address')
        website = request.POST.get('website')
        image_file = request.FILES['image']
        alphanumeric_characters = string.ascii_letters + string.digits
        image_name =''.join(random.choice(alphanumeric_characters) for _ in range(10))
        card = image_file.read()
        phone2 = request.POST.get('phone2')
        description= request.POST.get('description')
        image_file1 = request.FILES['image']
        image_name1 =''.join(random.choice(alphanumeric_characters) for _ in range(10))
        logo = image_file1.read()

        obj1=company.objects.all(email=email1)
        obj1.email = email1
        obj1.name = name
        obj1.phone = phone
        obj1.address = address
        obj1.website = website
        obj1.image_name = image_name
        obj1.card = card
        obj1.phone2 = phone2
        obj1.description = description
        obj1.image_name1 = image_name1
        obj1.logo = logo
        
        return redirect('/')
    return render(request, 'Sign-Up.html')
            
@ratelimit(key='ip', rate='10/m')
def volunteerinfo(request):
    if request.method == 'POST' and request.FILES['image']:
        email1 = request.COOKIES.get('email')
        name = request.COOKIES.get('name')
        phone = request.COOKIES.get('phone')
        dob = request.POST.get('dob')
        timestamp = date.today()
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')
        qualification = request.POST.get('qualification')
        emergency_contact = request.POST.get('emergency_contact')
        image_file = request.FILES['image']
        alphanumeric_characters = string.ascii_letters + string.digits
        image_name =''.join(random.choice(alphanumeric_characters) for _ in range(10))
        profile_pic = image_file.read()
        image_file1 = request.FILES['image']
        image_name1 =''.join(random.choice(alphanumeric_characters) for _ in range(10))
        id_proof = image_file1.read()
        upi = request.POST.get('upi')

        obj1=volunteer.objects.all(email=email1)
        obj1.email=email1
        obj1.name=name
        obj1.phone=phone
        obj1.dob = dob
        obj1.timestamp = timestamp
        obj1.experience = experience
        obj1.skills = skills
        obj1.qualification = qualification
        obj1.emergency_contact = emergency_contact
        obj1.image_name = image_name
        obj1.profile_pic = profile_pic
        obj1.image_name1 = image_name1
        obj1.card = id_proof
        obj1.upi = upi
        
        return redirect('/')
    return render(request, 'Sign-Up.html')

@ratelimit(key='ip', rate='10/m')
def logout(request):
    if 'email' and 'role' in request.session:
        request.session.pop('email')
        request.session.pop('role') 
        request.session.flush()

        return redirect('/')
    return redirect('/')


@ratelimit(key='ip', rate='10/m')
def reset(request):
    if request.method=="POST":
        email=request.POST.get('email')
        user=users.objects.get(email=email)
        load_dotenv()
        if user.length==0:
            return redirect('/auth/login')

        from_email=os.getenv('EMAIL')
        password=os.getenv('PASSWORD')

        email=user.email
        subject="Reset Password"
        length=8
        x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
        expiry_duration = timedelta(minutes=5)  # Set OTP validity duration
        expires_at = timezone.now() + expiry_duration
        resetpass1=resetpass(email=email,keys=x,usage=False,expires_at=expires_at)
        resetpass1.save()
        final_str_link="http://http://127.0.0.1:8000/auth/resetpass?email="+email+"&key="+x

        body=f"""
        <h1 style="text-align:center">One Time Password For Sign-in</h1>

                    <p>We're sorry to hear that you're having trouble with logging in to Any Time Event. We've received a message that you've forgotten your password. <br>
                    If this was you, you can reset your password now using this link . </p>

                    <h2>Your Link : {final_str_link}</h2>

                    <p>
                    If you didn't request password reset link, you can ignore this message
                
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
   

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, email, msg.as_string())
                
    return render(request, 'reset.html')

@ratelimit(key='ip', rate='10/m')
def resetpass(request):
    
    email=request.GET.get('email')
    key=request.GET.get('key')

    user=resetpass.objects.get(email=email,keys=key)

    if user.usage==True or user.is_expired():
        return redirect('/auth/login')
    
    else:
        return render(request, 'resetpass.html')
