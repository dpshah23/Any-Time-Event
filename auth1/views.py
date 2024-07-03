from django.shortcuts import render,redirect,HttpResponse,reverse
from django.http import HttpResponseRedirect
from .models import *
from cryptography.fernet import Fernet
from django.utils import timezone
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
        otp1=request.POST.get('o1')
        otp2=request.POST.get('o2')
        otp3=request.POST.get('o3')
        otp4=request.POST.get('o4')
        otp5=request.POST.get('o5')
        otp6=request.POST.get('o6')

        fianlotp=otp1+otp2+otp3+otp4+otp5+otp6
        email=request.session.get('email12')
        try:
            user=otps.objects.get(email=email,expires_at__gt=timezone.now())
            # print(user.otp)
            # print(otp)
            # print(email)
            if user.otp==int(fianlotp) and not user.is_expired():

                if users.objects.get(email=email).role=="volunteer" and users.objects.get(email=email).is_active!= False:
                    context={

                    }

                    response=redirect('/',context) 
                    response.set_cookie('time', 'true', max_age=15*24*60*60)
                    response.set_cookie('email', email, max_age=15*24*60*60)
                    response.set_cookie('Logged_in', 'true', max_age=15*24*60*60)

                    # print("cookie set")

                    request.session['email']=email
                    request.session['role']=users.objects.get(email=email).role
                    user.delete()
                    return response
                elif users.objects.get(email=email).role=="company" and users.objects.get(email=email).is_active!= False:
                
                    context={

                    }

                    response=render(request, 'home.html',context) 
                    response.set_cookie('time', 'true', max_age=15*24*60*60)
                    response.set_cookie('email', email, max_age=15*24*60*60)
                    response.set_cookie('Logged_in', 'true', max_age=15*24*60*60)

                    # print("cookie set")

                    request.session['email']=email
                    request.session['role']=users.objects.get(email=email).role
                    user.delete()
                    return response
                else:
                    user.delete()
                    return response
            else:
                messages.error(request, 'Invalid OTP')
                return render(request, 'OTP.html')
            
        except otps.DoesNotExist:
            messages.error(request,"OTP Expired")
            return redirect('/auth/login')
        

    return render(request, 'OTP.html')

def decrypt_password(password,key):

    try:
        decoded_key = base64.b64decode(key)
        decoded_password = base64.b64decode(password)

        f = Fernet(decoded_key)
   
        decrypted_password = f.decrypt(decoded_password)
    
        return decrypted_password.decode()
    except Exception as e:
        print(e)
        return None

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
            print(user)
           
            role=user.role
            # print(user)
            decrypted_pass=decrypt_password(user.password,user.key)
            if decrypted_pass==None:
                messages.error(request, 'Invalid Credentials')
                return render(request, 'Log-In.html')
            # print(decrypted_pass)
    
            if user.email==email and decrypted_pass==password and users.objects.get(email=email).is_active!= False :
                

                if  request.COOKIES.get('time'):
                    request.session['email']=email
                    request.session['role']=users.objects.get(email=email).role
                    context={

                    }

                    response=redirect( '/',context) 
                    response.set_cookie('time', 'true', max_age=15*24*60*60)
                    response.set_cookie('email', email, max_age=15*24*60*60)
                    response.set_cookie('Logged_in', 'true', max_age=15*24*60*60)


                    if role=="volunteer":
                        
                        return response
                    elif role=="company":
                        return response
                    else:
                        return response
                    
                
                load_dotenv()
                from_email=os.getenv('EMAIL')
                password=os.getenv('PASSWORD1')

                print(from_email,password)


                subject="One Time Password For Admin "
                length=8
                otp=random.randint(111111,999999)
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
                print(user1.otp)
                request.session['email12']=email

                print(True)
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(from_email, password)
                    server.sendmail(from_email, email, msg.as_string())
                    print("OTP Send Successfully")

                    print("mail sent")
                        
                    messages.success(request, 'OTP sent to your email')
                    return redirect('/auth/validate')
                

            else:
                messages.error(request, 'Incorrect E-mail or Password')
                return render(request, 'Log-In.html')

        except users.DoesNotExist:
            messages.error(request, 'Email Does Not Exist')
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
        messages.success(request, 'Company Registered Successfully')
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

        messages.success(request, 'Volunteer Registered Successfully')
        
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
    if request.method == "POST":
        email = request.POST.get('email')
        try:

            user = users.objects.filter(email=email)
            print(email)
            print(user)
            load_dotenv()

            from_email = os.getenv('EMAIL')
            password = os.getenv('PASSWORD1')

            subject = "Reset Password"
            length = 8
            x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
            expiry_duration = timedelta(minutes=5)  # Set OTP validity duration
            expires_at = timezone.now() + expiry_duration
            resetpass1 = resetpass(email=email, keys=x, usage=False, expires_at=expires_at)
            resetpass1.save()
            final_str_link = "http://127.0.0.1:8000/auth/resetpass?email=" + email + "&key=" + x

            body = f"""
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

            messages.success(request, 'Reset link sent to your email')
            return redirect('/auth/login')
        except users.DoesNotExist:
            messages.error(request, 'Invalid Email')
            return render(request, 'reset.html')
        
        except Exception as e:
            print(e)
            messages.error(request, 'Invalid Email')
            return render(request, 'reset.html')

    return render(request, 'reset.html')



@ratelimit(key='ip', rate='10/m')
def reset_pass(request):
    if request.method == "GET":
        email = request.GET.get('email')
        key = request.GET.get('key')
        # print(f"Received email: {email}, key: {key}")  # Debugging

        try:
            user_reset = resetpass.objects.get(email=email, keys=key)
            # print(f"Reset entry found: {user_reset}")  # Debugging

            if user_reset.usage or user_reset.is_expired():
                print("Invalid Link: Link is either used or expired")  # Debugging
                messages.error(request, 'Invalid Link')
                return redirect('/auth/login')
            
        except resetpass.DoesNotExist:
            print(f"No reset entry found for email: {email} and key: {key}")  # Debugging
            messages.error(request, 'Invalid reset link')
            return redirect('/auth/login')

    elif request.method == "POST":
        new_pass = request.POST.get('password')
        email = request.POST.get('email')
        key=request.POST.get('key')
        # print(f"New password received for email {email}: {new_pass}")  # Debugging

        try:
            user = users.objects.get(email=email)
            # print(f"User found: {user}")  # Debugging
            user_reset = resetpass.objects.get(email=email, keys=key)
            # Generate a new encryption key and encrypt the new password
            key1 = Fernet.generate_key()
            f = Fernet(key1)
            new_encrypt_pass = f.encrypt(new_pass.encode())
            encrypted_password = base64.b64encode(new_encrypt_pass).decode('utf-8')
            key_str = base64.b64encode(key1).decode('utf-8')

            # Update user's password and key
            user.password = encrypted_password
            user.key = key_str
            user.save()

            # Mark the reset pass entry as used
            user_reset.usage = True
            user_reset.save()

            return redirect('/auth/login')
        
        except users.DoesNotExist:
            # print(f"User with email {email} does not exist.")  # Debugging
            messages.error(request, 'User does not exist')
            return render(request, 'Reset_Password.html', {'email': email})
        
        except Exception as e:
            # print(f"Error resetting password: {str(e)}")  # Debugging
            messages.error(request, 'Error resetting password. Please try again.')
            return render(request, 'Reset_Password.html', {'email': email})

    return render(request, 'Reset_Password.html')