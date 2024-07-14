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
import requests
from datetime import timedelta
import json
import base64
import emailvalidationio


# Create your views here.
"""
Function: validate(request)
---------------------------

Description:
    This function handles OTP validation and user authentication based on the OTP entered
    by the user. It verifies the OTP against the stored OTP for the user, checks user role
    and activation status, sets session variables and cookies upon successful authentication,
    and deletes the OTP record from the database.

Parameters:
    request (HttpRequest): The HTTP request object containing POST data.

Returns:
    HttpResponse: Returns an appropriate HTTP response based on the validation result.
                  - Redirects to '/' for volunteers upon successful validation.
                  - Renders 'home.html' for companies upon successful validation.
                  - Renders 'OTP.html' with error message for invalid OTP.
                  - Redirects to '/auth/login' if OTP is expired or user does not exist.

Usage:
    This function is typically used in a Django view to process OTP validation during a
    user login flow.
"""
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

"""
Decrypts a password encoded with Fernet symmetric encryption using the provided key.

Parameters:
    password (str): Base64 encoded password string to decrypt.
    key (str): Base64 encoded key used for encryption and decryption.

Returns:
    str or None: Decrypted password as a string if successful, otherwise None.
"""
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
    
"""
Handles user login authentication and OTP generation and sending.

If session contains 'email' and 'role', redirects to '/'.
If request method is POST:
    - Retrieves email and password from POST data.
    - Checks if user is active and verifies credentials.
    - Redirects to '/' with session and cookies set upon successful login.
    - Generates and sends OTP via email for additional verification if needed.

Parameters:
    request (HttpRequest): The HTTP request object containing POST data for login.

Returns:
    HttpResponse: Renders 'Log-In.html' with appropriate error messages or redirects to '/'.

Exceptions:
    users.DoesNotExist: Raised if the user with the provided email does not exist.

"""
@ratelimit(key='ip', rate='10/m')
def login(request):
    if 'email' and 'role' in request.session:
        return redirect('/')
    
#     if request.method=="POST":
#         email=request.POST.get('email')
#         try:
#             if company.objects.get(email=email, phone2__isnull=True):
#                 print(email)
#                 messages.error(request, 'Please enter an email address with all the details.')
#                 return render(request, 'Log-In.html')
#             elif volunteer.objects.get(email=email, dob__isnull=True):
#                 print(email)
#                 messages.error(request, 'Please enter an email address with all the details.')
#                 return render(request, 'Log-In.html')
#             else :
#                 messages.error(request, 'Email Does Not Exist.....')
#                 return render(request, 'Log-In.html')
#         except (company.DoesNotExist, volunteer.DoesNotExist):
#             messages.error(request, 'Email Does Not Exist')
#             return render(request, 'Log-In.html')
    
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        email_exists = False

        try:
            if company.objects.get(email=email, phone2__isnull=True):
                print(email)
                messages.error(request, 'Please Sign up again with complete details after 5 minutes.')
                return render(request, 'Log-In.html')
            email_exists = True
        except company.DoesNotExist:
            pass
        
        try:
            if volunteer.objects.get(email=email, dob__isnull=True):
                print(email)
                messages.error(request, 'Please Sign up again with complete details after 5 minutes.')
                return render(request, 'Log-In.html')
            email_exists = True
        except volunteer.DoesNotExist:
            pass
        
        # if not email_exists:
        #     messages.error(request, 'Email Does Not Exist.')
        #     return render(request, 'Log-In.html')
        
        try:
            # print(1)
            user=users.objects.get(email=email)
            print(user)

            if user.block==True:
                messages.error(request,"Some Unexpected Activity happened in Your Account.. So We have Blocked Your Account")
                return redirect('/')

            if user.is_active==False:
                messages.error(request, 'Account is not activated... We Will Take 2 Working Days To Activate Your Account. Please Try Again Later.')
                return render(request, 'Log-In.html')
           
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


                subject="One Time Password For Login "
                length=8
                otp=random.randint(111111,999999)
                body=f"""

                <div style="font-family: Arial, sans-serif; color: #333;">
        <h1 style="text-align: center; color: #4CAF50;">One-Time Password for Secure Login</h1>

        <p>Dear User,</p>

        <p>
            We are thrilled to welcome you back to our platform! It has been over 15 days since your last login, and for your security, we need to verify your device.
        </p>

        <p>
            To proceed with the login process, please use the One-Time Password (OTP) provided below. This OTP is unique to your login attempt and will expire in 10 minutes for security purposes.
        </p>

        <div style="text-align: center; margin: 20px 0;">
            <h2 style="display: inline-block; background: #f4f4f4; padding: 10px 20px; border: 1px solid #ddd; border-radius: 5px;">{otp}</h2>
        </div>

        <p>
            Enter this OTP on the login page to verify your identity and continue accessing your account.
        </p>

        <p>
            If you did not request this login, please ignore this message. No further action is required.
        </p>

        <p>
            Should you have any questions or need assistance, please feel free to contact our team.
        </p>

        <p>
            Thank you for choosing Any Time Event. We are committed to ensuring the security and privacy of your account.
        </p>

        <p>
            Best regards,<br>
            <strong>The Any Time Event Team</strong>
        </p>
    </div>

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
                        
                    # messages.success(request, 'OTP sent to your email')
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

"""

Function: key()

Description:
    This function generates a random encryption key using Fernet symmetric encryption.
    
"""
def key():
    
    return Fernet.generate_key()

"""
Handles user registration process by encrypting password and saving user details.

If request method is POST:
    - Retrieves email, password, name, phone, and role from POST data.
    - Encrypts password using Fernet symmetric encryption.
    - Saves user details in the database based on role ('company' or 'volunteer').
    - Redirects to '/auth/companyinfo' or '/auth/volunteerinfo' based on role after successful registration.

Parameters:
    request (HttpRequest): The HTTP request object containing POST data for user registration.

Returns:
    HttpResponse: Redirects to '/auth/companyinfo' or '/auth/volunteerinfo' after successful registration.
                  Renders 'Sign-Up.html' with error message if email is already registered.

"""
@ratelimit(key='ip', rate='10/m')
def signup (request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # load_dotenv()
        # api=os.getenv('api_key_email_validation')
        # print(api)

        # client = emailvalidationio.Client(api)
        
        # result=client.validate(email)

        # print(result)
        # if result['mx_found'] is False or result['smtp_check'] is False or result['reason'] == 'invalid_mailbox':
        #     messages.error(request, 'Invalid Email')
        #     return redirect('/auth/signup')
        

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
        
        if role=="company":
            user1 = users(email=email,password=encrypted_password,key=key_str,role=role,timestamp=date.today())
            user1.save()
        else:
            user1 = users(email=email,password=encrypted_password,key=key_str,role=role,is_active=True,timestamp=date.today())
            user1.save()
            
        print("hello")

        keyid=x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        if role == "company":
            print("in company")

            c1=company(name=name,email=email,phone1=phone,comp_id=keyid)
            c1.save()
            return redirect('/auth/companyinfo')
        else:
            print("in volunterr")
            v1 = volunteer(name=name ,email=email,phone=phone,vol_id=keyid )
            v1.save()
            return redirect('/auth/volunteerinfo')
       
        
    return render(request, 'Sign-Up.html')


"""
Handles the registration process for companies, including company profile information and file uploads.

If request method is POST:
    - Validates and processes uploaded images for company card and logo.
    - Validates file extensions for JPG, PNG, JPEG, and HEIC formats.
    - Saves company details and uploaded files to the database.
    - Redirects to '/' upon successful registration.

Parameters:
    request (HttpRequest): The HTTP request object containing POST data for company registration.

Returns:
    HttpResponse: Redirects to '/' after successful registration. Renders 'company_data.html' with error messages
                  if required fields are missing or if there are validation errors.

Notes:
    This function assumes the use of Django framework for web development.
    Handles file uploads and validates file extensions for security.
"""

@ratelimit(key='ip', rate='10/m')
def companyinfo(request):

    if not request.session.get('email123') or not request.session.get('phone123') or not request.session.get('name123'):
        messages.error(request, "You are not authorized to access this page")
        return redirect('/')

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
        try:
            card = base64.b64encode(image_file.read()).decode('utf-8')
            logo = base64.b64encode(image_file1.read()).decode('utf-8')
        except Exception as e:
            messages.error(request, 'Error processing image files: {}'.format(str(e)))
            return render(request, 'company_data.html')
        
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

        request.session.pop('email123')
        request.session.pop('phone123')
        request.session.pop('name123')


        messages.success(request, 'Company Registered Successfully')
        return redirect('/')
    
    return render(request, 'company_data.html')


"""
Handles the registration process for volunteers, including profile information and Razorpay integration.

If request method is POST:
    - Validates and processes uploaded images for profile picture and identity proof.
    - Validates file extensions and checks Razorpay credentials.
    - Creates Razorpay contact and fund account for the volunteer.
    - Saves volunteer details and uploaded files to the database.
    - Redirects to '/' upon successful registration.

Parameters:
    request (HttpRequest): The HTTP request object containing POST data for volunteer registration.

Returns:
    HttpResponse: Redirects to '/' after successful registration. Renders 'user_data.html' with error messages
                  if required fields are missing or if there are validation errors.

Notes:
    This function assumes the use of Django framework for web development.
    Requires integration with Razorpay for contact and fund account creation.
"""
@ratelimit(key='ip', rate='10/m')
def volunteerinfo(request):

    if not request.session.get('email123') or not request.session.get('phone123') or not request.session.get('name123'):
        messages.error(request, "You are not authorized to access this page")
        return redirect('/')
    

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
        city=request.POST.get('city')
        
        
        # Generate random image names
        alphanumeric_characters = string.ascii_letters + string.digits
        image_name = ''.join(random.choice(alphanumeric_characters) for _ in range(10))
        image_name1 = ''.join(random.choice(alphanumeric_characters) for _ in range(10))
        
        image_file = request.FILES['profile_picture'].read()
        image_file1 = request.FILES['identity_proof'].read()
        # Read image files
        try:    
            profile_pic = base64.b64encode(image_file).decode('utf-8')
            id_proof = base64.b64encode(image_file1).decode('utf-8')
            # print(profile_pic)
            # print()
            # print("hello")
            # print(id_proof)
        except Exception as e:
            messages.error(request, 'Error processing image files: {}'.format(str(e)))
            return render(request, 'user_data.html')
        load_dotenv()
        api_key = os.getenv('api_key')   
        api_secret = os.getenv('api_secret')
        print(api_key)
        print(api_secret)
        
        
        if not api_key and not api_secret:
            messages.error(request, 'Payment gateway credentials not set. Please contact support.')
            return render(request, 'user_data.html')
        
        contact_url = "https://api.razorpay.com/v1/contacts"

        payload = {
        "name": name,
        "email": email1,
        "contact": phone,
        "type": "customer",
        "reference_id": "123",
        "notes": {
        "notes_key_1": "123",
        "notes_key_2": "123"
        }
        }

        print(payload)
        
        payload_json = json.dumps(payload)
        # print(payload_json)

        headers = {
        "Content-Type": "application/json"
        }

        response = requests.post(contact_url, auth=(api_key,api_secret), data=payload_json, headers=headers)

        print(response.json())

        if response.json()['id']:
            print("Contact Created Successfully")
            
            contact_id = response.json()['id']
        else:
            print("Error creating contact")
        

        url_fund = "https://api.razorpay.com/v1/fund_accounts"

        payload_fund = {
        "contact_id": contact_id,  # Replace with the actual contact_id obtained from the previous step
        "account_type": "vpa",
        "vpa": {
            "address": upi
        }
        }
        
        payload_json_fund = json.dumps(payload_fund)

        headers = {
        "Content-Type": "application/json"

        }

        response_fund = requests.post(url_fund, auth=(api_key, api_secret), data=payload_json_fund, headers=headers)
        print(response_fund.json())
        if response_fund.json()['id']:
            print("Fund Account Created Successfully")  
            fund_id = response_fund.json()['id']
        else:
            # print(response_fund.json())
            messages.error(request, f"Failed to create fund account: {response_fund.json().get('error', {}).get('description', 'Unknown error')}")
            return render(request, 'user_data.html')

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
                'contact_id': contact_id,
                'fund_id': fund_id,
                'city':city.lower()
            }
        )


        request.session.pop('email123')
        request.session.pop('phone123')
        request.session.pop('name123')

        
        messages.success(request, 'Volunteer Registered Successfully')
        
        return redirect('/')
    
    return render(request, 'user_data.html')

"""
Handles user logout by clearing session data.

If 'email' and 'role' are in session:
    - Removes 'email' and 'role' from session.
    - Flushes the session to clear all session data.
    - Redirects to '/'.

Returns:
    HttpResponse: Redirects to '/' after clearing session data.


"""
@ratelimit(key='ip', rate='10/m')
def logout(request):
    if 'email' and 'role' in request.session:
        request.session.pop('email')
        request.session.pop('role') 
    
        request.session.flush()

        return redirect('/')
    return redirect('/')


"""
Handles the password reset request process.

If request method is POST:
    - Retrieves email from POST data.
    - Generates a unique reset key and saves it with an expiry time.
    - Sends a reset link to the user's email with the generated key.
    - Redirects to '/auth/login' upon successful sending of the reset link.

Parameters:
    request (HttpRequest): The HTTP request object containing POST data for password reset request.

Returns:
    HttpResponse: Redirects to '/auth/login' after sending the reset link. Renders 'reset.html' with error messages
                  if the email is invalid or if there are any errors during the process.

Notes:
    Requires SMTP configuration for sending emails and uses environment variables for email credentials.
"""
@ratelimit(key='ip', rate='10/m')
def reset(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = users.objects.get(email=email)
            
        except users.DoesNotExist:
            messages.error(request, 'Invalid Email')
            return render(request, 'reset.html')
        except Exception as e:
            print(e)
            messages.error(request, 'Invalid Email')
            return render(request, 'reset.html')
        try:
            load_dotenv()

            from_email = os.getenv('EMAIL')
            password = os.getenv('PASSWORD1')

            subject = "Reset Password"
            length = 8
            x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(32))
            expiry_duration = timedelta(hours=1)  # Set OTP validity duration
            expires_at = timezone.now() + expiry_duration
            resetpass1 = resetpass(email=email, keys=x, usage=False, expires_at=expires_at)
            resetpass1.save()
            final_str_link = "http://127.0.0.1:8000/auth/resetpass?email=" + email + "&key=" + x

            body = f"""
            <div style="font-family: Arial, sans-serif; color: #333;">
    <h1 style="text-align: center; color: #4CAF50;">Password Reset Request</h1>

    <p>Dear User,</p>

    <p>We understand that you are having trouble logging into your Any Time Event account. To help you get back on track, we have received a request to reset your password.</p>

    <p>If you initiated this request, you can reset your password by clicking the link below. For security reasons, this link will expire in 1 hour:</p>

    <div style="text-align: center; margin: 20px 0;">
        <h2 style="display: inline-block; background: #f4f4f4; padding: 10px 20px; border: 1px solid #ddd; border-radius: 5px;">
            <a href="{final_str_link}" style="text-decoration: none; color: #4CAF50;">Reset Password</a>
        </h2>
    </div>

    <p>If you did not request a password reset, please ignore this message. Your account will remain secure, and no changes will be made.</p>

    <p>If you have any questions or need further assistance, please do not hesitate to contact our team.</p>

    <p>Thank you for your understanding and cooperation.</p>

    <p>Best regards,<br><strong>The Any Time Event Team</strong></p>
</div>
            
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


"""
Handles password reset process based on email link verification and new password submission.

If request method is GET:
    - Retrieves email and key parameters from the request query.
    - Checks if a valid reset entry exists for the provided email and key.
    - If the reset link is invalid (used or expired), redirects to '/auth/login' with an error message.

If request method is POST:
    - Retrieves new password, email, and key from the POST data.
    - Decrypts the existing reset entry to validate and update the user's password.
    - Generates a new encryption key, encrypts the new password, and updates the user's password and key in the database.
    - Marks the reset entry as used.
    - Redirects to '/auth/login' upon successful password reset.

Parameters:
    request (HttpRequest): The HTTP request object containing GET or POST data for password reset.

Returns:
    HttpResponse: Redirects to '/auth/login' after successful password reset or renders 'Reset_Password.html' with error messages
                  if the reset link is invalid or if there are errors during the process.

Notes:
    This function assumes the use of Django framework for web development.
    Uses Fernet encryption for securely storing passwords.
"""
@ratelimit(key='ip', rate='10/m')
def reset_pass(request):
    if request.method == "GET":
        email = request.GET.get('email')
        key = request.GET.get('key')
        # print(f"Received email: {email}, key: {key}")  # Debugging

        try:
            user_reset = resetpass.objects.get(email=email, keys=key)
            # print(f"Reset entry found: {user_reset}")  # Debugging

            if user_reset.usage:
                messages.error(request,"Link Is Already Used")
                return redirect('/auth/login')
            elif user_reset.is_expired():
                print("Invalid Link: Link is Expired")  # Debugging
                messages.error(request, 'Link is expired')
                return redirect('/auth/login')
            
        except resetpass.DoesNotExist:
            print(f"No reset entry found for email: {email} and key: {key}")  # Debugging
            messages.error(request, 'Invalid reset link or Link Already Used')
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

            user_reset.delete()

            return redirect('/auth/login')
        
        except resetpass.DoesNotExist:
            # print(f"Reset entry not found for email: {email}")  # Debugging
            messages.error(request, 'Invalid reset link')
            return render(request, 'Reset_Password.html')
        
        except users.DoesNotExist:
            # print(f"User with email {email} does not exist.")  # Debugging
            messages.error(request, 'User does not exist')
            return render(request, 'Reset_Password.html', {'email': email})
        
        except Exception as e:
            # print(f"Error resetting password: {str(e)}")  # Debugging
            messages.error(request, 'Error resetting password. Please try again.')
            return render(request, 'Reset_Password.html', {'email': email})

    return render(request, 'Reset_Password.html')

