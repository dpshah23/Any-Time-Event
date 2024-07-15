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
import requests
from datetime import datetime
from .models import payout
from django.http import HttpResponse as httpresponse

# Create your views here.
'''
Function Name:
accept_user

Description:
This view function retrieves active volunteers and inactive companies to prepare them for acceptance or further processing. 
It filters out unwanted company and volunteer entries based on certain conditions and prepares the final lists for rendering in the
template. The function then renders the accept_vol.html template with the context data.

Parameters:
request: The HTTP request object containing metadata about the request and user data.

Returns:
Renders the accept_vol.html template with the context data containing lists of volunteers and companies.

Usage:
This function is intended to be used in a Django web application as a view for displaying lists of volunteers and companies that need to be accepted or processed.
'''
def accept_user(request):
    # Fetch volunteers who are not expired
    vols = users.objects.filter(role="volunteer").filter(is_active=True)
    
    # Fetch companies
    comps = users.objects.filter(role="company",is_active=False)
    
    final_vols = []
    final_comps = []

    companys_unwanted=company.objects.filter(phone2__isnull=True)

    volunteer_unwanted=volunteer.objects.filter(dob__isnull=True)
    for comp in comps:
        try:
            
            compobj = company.objects.get(email=comp.email)
            # print(compobj.logo)
            
            final_comps.append((compobj))
        except company.DoesNotExist:
            pass
      
            
    
    # Retrieve volunteer objects based on their email and prepare for context
    for user in vols:
        try:
            if user.is_expired():
                volobj = volunteer.objects.get(email=user.email)

                final_vols.append( volobj )


        except volunteer.DoesNotExist:
            pass  # Handle case where volunteer object does not exist
    
    print(final_vols)
    print(final_comps)

    
    context = {
        'volunteers': final_vols,
        'companys': final_comps,
        'companys_unwanted':companys_unwanted,
        'volunteers_unwanted':volunteer_unwanted
    }
    
    return render(request, 'accept_vol.html', context)

'''
Function Name:
pay

Description:
This view function retrieves and categorizes events based on their payment status for volunteers and companies. It organizes events into 
three categories:

    1. Events where volunteer payments are pending but company payments are completed.
    2. Events where both volunteer and company payments are completed.
    3. Events where both volunteer and company payments are pending but the event date has passed.

The function then renders the event_payment.html template with the categorized event data.

Parameters:
request: The HTTP request object containing metadata about the request and user data.

Returns:
Renders the event_payment.html template with the context data containing categorized event lists.

Usage
This function is intended to be used in a Django web application as a view for displaying the payment status of events. 
'''

@login_required(login_url='/dj-admin/')
def pay(request):
    rem_payment=Event.objects.filter(is_paid_vol=False,paid_status=True)

    complete_payment=Event.objects.filter(is_paid_vol=True,paid_status=True)

    event_complete_payment_undone=Event.objects.filter(is_paid_vol=False,paid_status=False)
    final_event_complete_payment_undone=[]
    for event in event_complete_payment_undone:
        
        days=(date.today()-event.event_date).days
        if days>0:

            final_event_complete_payment_undone.append((event,days))

    # print(final_event_complete_payment_undone)

    context={
        'events_ex': rem_payment,
        'complete_payment': complete_payment,
        'unpaid_company': final_event_complete_payment_undone
    }
    return render(request, 'event_payment.html',context)

'''

Function Name:
acceptyes

Description:
This view function activates a user account based on the provided email and sends an authorization email to the user, 
notifying them that their account has been successfully authorized. The function also handles the email sending process using
environment variables for the email credentials.

Parameters:
    request: The HTTP request object containing metadata about the request and user data.
    volemail: The email address of the user to be activated.

Returns:
Redirects to the accept users page ('/admincustom/acceptusers') with a success message.

Usage:
This function is intended to be used in a Django web application as a view for accepting and activating user accounts.
'''

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

    <div style="font-family: Arial, sans-serif; color: #333;">
    <h1 style="text-align:center; color: #4CAF50;">Authorization Successful</h1>

    <p>Dear User,</p>

    <p>Thank you for registering on our website, Any Time Event. We are pleased to inform you that your account has been successfully authorized. You can now log in to our site using your credentials.</p>
    
    <p>To ensure the security of your account, please enter the One-Time Password (OTP) that will be provided to you at the login page to verify your identity.</p>

    <p>If you have any questions or require further assistance, please do not hesitate to contact our team . We are here to help and ensure your experience with Any Time Event is smooth and enjoyable.</p>

    <p>Thank you for choosing Any Time Event. We look forward to your active participation and support.</p>

    <p>Best regards,<br><strong>The Any Time Event Team</strong></p>
</div>

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
    return redirect('/admincustom/acceptusers')

'''
Function Name:
acceptno

Description:
This view function deactivates a user account based on the provided email and sends a rejection email to the user,
notifying them that their registration attempt was unsuccessful. It also deletes the corresponding user data from the database.
The function handles the email sending process using environment variables for the email credentials.

Parameters:
    request: The HTTP request object containing metadata about the request and user data.
    volemail: The email address of the user to be rejected.
    
Returns:
Redirects to the accept users page ('/admincustom/acceptusers') with a rejection message.

Usage:
This function is intended to be used in a Django web application as a view for rejecting user accounts. 
'''
    
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

    <div style="font-family: Arial, sans-serif; color: #333;">
    <h1 style="text-align:center; color: #d9534f;">Authorization Attempt Failed</h1>
    
    <p>Dear Applicant,</p>
    
    <p>Thank you for registering on our website, Any Time Event. We appreciate your interest in joining our community. However, we regret to inform you that your registration has not been successful at this time.</p>
    
    <p>After a careful review of the details you provided, we have found some discrepancies that prevent us from approving your account. We encourage you to verify your information and try registering again. Ensuring that all provided information is accurate and complete can help facilitate a smoother registration process.</p>
    
    <p>If you have any questions or need further assistance, please do not hesitate to contact our team to address any concerns or queries you may have.</p>
    
    <p>We value your effort and time, and we hope that you will take the opportunity to rectify the issues and attempt registration once more. We look forward to welcoming you to our community and to your active participation in our events.</p>
    
    <p>Thank you for your time and understanding.</p>
    
    <p>Best regards,<br><strong>The Any Time Event Team</strong></p>
</div>


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

'''
Function Name
payvol

Purpose :

Description
The payvol view function handles the process of paying volunteers for their participation in a specific event. 
It retrieves registered volunteer details for a given event where attendance is marked as "present" and the payment status is false.
Using Razorpay's API, it initiates payouts to each volunteer's account based on their associated fund ID. Upon successful payment 
processing, it updates the volunteer's payment status, logs the transaction details into a database table (payout), and sends a 
confirmation email to the volunteer.

Parameters:
request: The HTTP request object containing metadata about the request and user data.
event_id: The unique identifier of the event for which volunteer payments are being processed.

Returns:
Redirects to the /admincustom/pay page upon successful payment completion or failure, displaying appropriate success or error messages.

Detailed Steps:
    1. Retrieve Volunteer Details: 
        Fetches volunteer records (RegVol) for the specified event (event_id) where attendance is marked as "present" and payment status
        is false.

    2. Initialize Razorpay Credentials: 
        Loads API key and secret from environment variables for authentication with the Razorpay API.

    3. Iterate Through Volunteers: For each volunteer:
        - Constructs a data payload for the payout transaction including account details, amount, currency, mode, purpose, and notes.
        - Sends a POST request to Razorpay's payout endpoint (payouts) to process the payment.
        - Upon successful payment (status_code == 200):
        - Updates the volunteer's payment status to true (paid_status=True).
        - Logs the transaction details (timestamp, event_name, vol_id, vol_email, event_id, rz_id, entity, amount, mode) into the payout database table.
        - Sends a confirmation email to the volunteer acknowledging the successful payment.
        - If payment fails (status_code != 200), logs the failure but continues processing.
        
    4. Update Event Payment Status: If all payments are successful (all_paid=True):
        - Marks the event (Event) as fully paid for volunteers (is_paid_vol=True).
        - Displays a success message and redirects to the /admincustom/pay page.
        
    5. Handle Payment Failure: 
        If any payment fails, displays an error message and redirects to the /admincustom/pay page.

Usage :
This function is crucial in managing the financial aspects of event participation for volunteers.
It integrates with Razorpay for secure payment processing and ensures that volunteers are compensated accurately and promptly for
their contributions to events.
'''
    

def payvol(request,event_id):
    regvoldetails=RegVol.objects.filter(event_id_1=event_id,attendence="present",paid_status=False)

    print(regvoldetails)
    load_dotenv()
    key=os.getenv('api_key')
    secret=os.getenv('api_secret')
    print(key)
    print(secret)
    all_paid=False
    payout_endpoint="https://api.razorpay.com/v1/payouts"
    for vol in regvoldetails:
        email_to=vol.email
        amount=Event.objects.get(event_id=event_id).actual_amount
        fano=volunteer.objects.get(email=email_to).fund_id
        print(email_to)
        print (fano)
        data={
        "account_number": '2323230032761492',
        "fund_account_id": fano,
        "amount": amount*100,
        "currency": "INR",
        "mode": "UPI",
        "purpose": "refund",
        "queue_if_low_balance": True,
        "reference_id": "Payment For Event",
        "narration": "Event Fund Transfer",
        "notes": {
            "notes_key_1":f"{event_id} - {email_to}",
            "notes_key_2":"Payment Done"
        }
        }

        print(data)
        headers={
            "Content-Type": "application/json",
            
            }
        response=requests.post(payout_endpoint,headers=headers,json=data,auth=(key,secret))

        print(response.json())

        if response.status_code==200:
            vol.paid_status=True
            vol.save()
            all_paid=True
            event_name = Event.objects.get(event_id=event_id).event_name

            timestamp=datetime.now().date().isoformat()

            obj1=payout(timestamp1=timestamp,event_name=event_name,vol_id=vol.vol_id,vol_email=vol.email,event_id=event_id,rz_id=response.json()['id'],entity=response.json()['entity'],amount=response.json()['amount'],mode=response.json()['mode'])
            obj1.save()

            load_dotenv()
            from_email=os.getenv('EMAIL')
            password=os.getenv('PASSWORD1')
            name=Event.objects.get(event_id=event_id).event_name
            amount=Event.objects.get(event_id=event_id).actual_amount
            subject=f"Payment For Event : {name}"

            body=f"""
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1 style="text-align:center; color: #4CAF50;">Payment Confirmation</h1>

                <p>Dear Participant,</p>

                <p>We are pleased to inform you that we have successfully processed your payment of <strong>{amount}</strong> for attending and participating in <strong>{name}</strong>.</p>

                <p>Thank you for your active participation and contribution to making the event a success. We hope you had a valuable and enjoyable experience.</p>

                <p>If you have any questions or need further assistance, please do not hesitate to contact us . We are here to help and support you with any inquiries you may have.</p>

                <p>We look forward to your continued participation in our future events.</p>

                <p>Best regards,<br><strong>The Any Time Event Team</strong></p>
            </div>
            """
            smtp_server = 'smtp.gmail.com'
            port = 587

            # Send the bulk email
            send_bulk_email(smtp_server, port, from_email, password, subject, body,email_to)


        else:
            print("payment Failed")
            all_paid=False
            
            pass
        
        if all_paid:
            event=Event.objects.get(event_id=event_id)
            event.is_paid_vol=True
            event.save()
            messages.success(request,"Payment Done")
            return redirect('/admincustom/pay')
        else:
            messages.error(request,"Payment Failed")
            return redirect('/admincustom/pay')

    

def send_bulk_email(smtp_server, port, sender_email, sender_password, subject, body,recipient):


    print("mail : ",recipient)
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  
    server.login(sender_email, sender_password)
   
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

      
    msg.attach(MIMEText(body, 'html'))

    server.sendmail(sender_email, recipient, msg.as_string())
    print(f"Email sent to {recipient}")


    server.quit()


def delete(request,email,role):
    try:
        users.objects.get(email=email).delete()

        if role=="volunteer":
            volunteer.objects.get(email=email).delete()
        
        else:
            company.objects.get(email=email).delete()
    
    except Exception as e:
        print(e)
        return redirect('/admincustom/acceptusers/')
        
    return redirect('/admincustom/acceptusers/')
    

# from company.models import company_payment
# def delete(request):
#     company_payment.objects.all().delete()
#     return httpresponse("Data Deleted")