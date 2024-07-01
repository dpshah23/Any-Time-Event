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
        email=request.session.get('email12')
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
            # print(1)
            user=users.objects.get(email=email)
            role=user.role
            # print(user)
            decrypted_pass=decrypt_password(user.password,user.key)
            # print(decrypted_pass)
            if user.email==email and int(decrypted_pass)==int(password):
                if role=="volunteer":
                       
                    return HttpResponse("Volunteer")
                elif role=="company":
                    return HttpResponse("Company")
                else:
                    redirect('/')
                    # print(True)
                
                    # load_dotenv()
                    # from_email=os.getenv('EMAIL1')
                    # password=os.getenv('PASSWORD1')

                    # print(from_email,password)


                    # subject="One Time Password For Admin "
                    # length=8
                    # otp=random.randint(000000,999999)
                    # body=f"""

                    # <h1 style="text-align:center">One Time Password For Sign-in</h1>

                    # <p>Thank you for registering on our website again but you need to confirm your device because it has been over 15 days since you last logged in .<br>
                    # To complete the registration process, please use the following One-Time Password (OTP) </p>

                    # <h2>Your OTP : {otp}</h2>

                    # <p>
                    # Please enter this OTP on the registration page to verify your identity and activate your account.

                    # If you did not initiate this registration, please ignore this message.
                
                    # </p>

                    # Thank you,
                    # <br>
                    # Any Time Event.

                    # """
                    # msg = MIMEMultipart()
                    # msg['Subject'] = subject
                    # msg['From'] = from_email
                    # msg['To'] = email
                    # msg.attach(MIMEText(body, 'html'))
                    # expiry_duration = timedelta(minutes=5)  # Set OTP validity duration
                    # expires_at = timezone.now() + expiry_duration
                    # user1=otps(email=email,otp=otp, expires_at=expires_at)
                    # user1.save()
                    # print(user1.otp)
                    # request.session['email12']=email

                    # print(True)
                    # with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    #     server.starttls()
                    #     server.login(from_email, password)
                    #     server.sendmail(from_email, email, msg.as_string())
                    #     print("OTP Send Successfully")

                    #     print("mail sent")
                        
                        
                    #     return redirect('/validate')
                

        #   else:
                messages.error(request, 'Invalid Credentials')
                return render(request, 'Log-In.html')

        except Exception as e:
            print(e)
            messages.error(request, 'Invalid Credentials')
            return render(request, 'Log-In.html')

    return render(request, 'Log-In.html')

def key():
    
    return Fernet.generate_key()


@ratelimit(key='ip', rate='10/m')
def signup (request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if users.objects.filter(email=email).exists():
                messages.info(request, 'Email already registered')
                return render(request, 'Sign-Up.html')
        
        password = request.POST.get('password')
        name = request.POST.get('name')
        phone = request.POST.get('contact_no')
        role = request.POST.get('role')
            
        key1=key()
        f=Fernet(key1)
        encrypt=f.encrypt(password.encode())
        encrypted_password = base64.b64encode(encrypt).decode('utf-8')
        key_str = base64.b64encode(key1).decode('utf-8')

         
        # response = HttpResponse("User Registered")
        # response.set_cookie('email', email, max_age=15*24*60*60)
        # response.set_cookie('name', name, max_age=15*24*60*60)
        # response.set_cookie('phone', phone, max_age=15*24*60*60)
        
        request.session['email123'] = email
        request.session['name123'] = name
        request.session['phone123'] = phone
        
        user1 = users(email=email,password=encrypted_password,key=key_str,role=role)
        user1.save()
        print("hello")
        if role == "company":
            print("in company")
            c1=company(name=name,email=email,phone1=phone)
            c1.save()
            return redirect('/auth/companyinfo')
        else:
            print("in volunterr")
            v1 = volunteer(name=name ,email=email,phone=phone )
            v1.save()
            return redirect('/auth/volunteerinfo')
       
        
    return render(request, 'Sign-Up.html')


@ratelimit(key='ip', rate='10/m')
def companyinfo(request):
    if request.method == 'POST':
        image_file = request.FILES.get('company_card')
        image_file1 = request.FILES.get('company_logo')
        
        # Validate file extensions
        valid_extensions = ['jpg', 'png', 'jpeg', 'heic']
        if not all(image.name.split('.')[-1].lower() in valid_extensions for image in [image_file, image_file1]):
            messages.error(request, 'Invalid Image format. Only JPG, PNG, JPEG, and HEIC are allowed.')
            return render(request, 'company_data.html')
        
        email1 = request.session.get('email123')
        name = request.session.get('name123')
        phone = request.session.get('phone123')
        address = request.POST.get('company_address')
        website = request.POST.get('website_company')
        
        # Generate random image names
        alphanumeric_characters = string.ascii_letters + string.digits
        image_name = ''.join(random.choice(alphanumeric_characters) for _ in range(10))
        image_name1 = ''.join(random.choice(alphanumeric_characters) for _ in range(10))
        
        # Read image files
        card = image_file.read()
        logo = image_file1.read()
        
        # Create or update company object
        obj, created = company.objects.update_or_create(
            email=email1,
            defaults={
                'name': name,
                'phone': phone,
                'address': address,
                'website': website,
                'image_name': image_name,
                'card': card,
                'phone2': request.POST.get('contact_no_2'),
                'description': request.POST.get('company_description'),
                'image_name1': image_name1,
                'logo': logo,
            }
        )
        
        return redirect('/')
    
    return render(request, 'company_data.html')

            

@ratelimit(key='ip', rate='10/m')
def volunteerinfo(request):
    if request.method == 'POST':
        # Check if both images are uploaded
        if 'profile_picture' not in request.FILES or 'identity_proof' not in request.FILES:
            messages.error(request, 'Both profile picture and identity proof are required')
            return render(request, 'user_data.html')

        image_file = request.FILES['profile_picture']
        image_file1 = request.FILES['identity_proof']
        
        # Validate file extensions
        valid_extensions = ['jpg', 'png', 'jpeg', 'heic']
        if not all(image.name.split('.')[-1].lower() in valid_extensions for image in [image_file, image_file1]):
            messages.error(request, 'Invalid Image format. Only JPG, PNG, JPEG, and HEIC are allowed.')
            return render(request, 'user_data.html')
        
        email1 = request.session.get('email123')
        name = request.session.get('name123')
        phone = request.session.get('phone123')
        dob = request.POST.get('dob')
        timestamp = date.today()
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')
        qualification = request.POST.get('qualification')
        emergency_contact = request.POST.get('emergency_no')
        upi = request.POST.get('upi_id')
        
        # Generate random image names
        alphanumeric_characters = string.ascii_letters + string.digits
        image_name = ''.join(random.choice(alphanumeric_characters) for _ in range(10))
        image_name1 = ''.join(random.choice(alphanumeric_characters) for _ in range(10))
        
        # Read image files
        profile_pic = image_file.read()
        id_proof = image_file1.read()
        
        # Create or update volunteer object
        obj, created = volunteer.objects.update_or_create(
            email=email1,
            defaults={
                'name': name,
                'phone': phone,
                'dob': dob,
                'timestamp': timestamp,
                'experience': experience,
                'skills': skills,
                'qualification': qualification,
                'emergency_contact': emergency_contact,
                'image_name': image_name,
                'profile_pic': profile_pic,
                'image_name1': image_name1,
                'card': id_proof,
                'upi': upi,
            }
        )
        
        return redirect('/')
    
    return render(request, 'user_data.html')

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
        if request.method=="POST":
            new_pass=request.POST.get('password')

            user=users.objects.get(email=email)

            key=user.key
            f=Fernet(key)
            new_encrypt_pass=f.encrypt(new_pass.encode())
            encrypted_password = base64.b64encode(new_encrypt_pass).decode('utf-8')
            
            user.password=encrypted_password

            user.save()


            return redirect('auth/login')



        return render(request, 'Reset_Password.html')
