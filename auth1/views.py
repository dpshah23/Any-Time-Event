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

def key():
    
    return Fernet.generate_key()

def signup (request):
    if request.method == 'POST':
        if users.objects.all (email!=email) :

            email = request.POST.get('email')
            password = request.POST.get('password')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            role = request.POST.get('role')
            
            key1=key()
            f=Fernet(key1)
            encrypt=f.encrypt(password.encode())
            encrypted_password = base64.b64encode(encrypt).decode('utf-8')
            key_str = base64.b64encode(key1).decode('utf-8')

            def set_cookie(request):
                response = HttpResponse("Cookie Set")
                response.set_cookie('email', email, max_age=3600) 
                return response
            user1 = users(email=email,password=encrypted_password,key=key_str,role=role)
            user1.save()
            
            if role == "company":
                c1=company(email=email,password=encrypted_password,key=key_str,role=role)
                return redirect('/companyinfo')
            else :
                v1 = volunteer(email=email,password=encrypted_password,key=key_str,role=role)
                return redirect('/volunteerinfo')
       
        else : 
            messages.error(request, 'Email Already Exist')
            return render(request, 'Sign-Up.html')
        return redirect('/')
    return render(request, 'Sign-Up.html')

def companyinfo(request):
    if request.method == 'POST':
        email1 = request.COOKIES.get('email')
        address = request.POST.get('address')
        website = request.POST.get('website')
        card = request.POST.get('card')
        phone2 = request.POST.get('phone2')
        description= request.POST.get('description')
        logo = request.POST.get('logo')

        obj1=company.objects.all(email=email1)
        obj1.address = address
        obj1.website = website
        obj1.card = card
        obj1.phone2 = phone2
        obj1.description = description
        obj1.logo = logo
            
def volunteerinfo(request):
    if request.method == 'POST':
        email1 = request.COOKIES.get('email')
        dob = request.POST.get('dob')
        timestamp = request.POST.get('timestamp')
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')
        qualification = request.POST.get('qualification')
        emergency_contact = request.POST.get('emergency_contact')
        profile_pic = request.POST.get('profile_pic')
        id_proof = request.POST.get('id_proof')
        upi = request.POST.get('upi')
        description = request.POST.get('de4scription')

        obj1=volunteer.objects.all(email=email1)
        obj1.email=email1
        obj1.dob = dob
        obj1.timestamp = timestamp
        obj1.experience = experience
        obj1.skills = skills
        obj1.qualification = qualification
        obj1.emergency_contact = emergency_contact
        obj1.profile_pic = profile_pic
        obj1.id_proof = id_proof
        obj1.upi = upi
        obj1.description = description




def logout(request):
    if 'email' and 'role' in request.session:
        request.session.pop('email')
        request.session.pop('role') 
        request.session.flush()

        return redirect('/')
    return redirect('/')


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
        resetpass1=resetpass(email=email,keys=x,usage=False)
        resetpass1.save()
        final_str_link="http://http://127.0.0.1:8000/auth/resetpass?email="+email+"&key="+x

        body=f"""
        <h1 style="text-align:center">One Time Password For Sign-in</h1>

                    <p>Thank you for registering on our website again but you need to confirm your device because it has been over 15 days since you last logged in .<br>
                    To complete the registration process, please use the following One-Time Password (OTP) </p>

                    <h2>Your OTP : {final_str_link}</h2>

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
   

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, email, msg.as_string())
                
    return render(request, 'reset.html')

def resetpass(request):
    
    password=request.POST.get('password')
    key=request.POST.get('key')