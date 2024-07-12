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
def accept_user(request):
    # Fetch volunteers who are not expired
    vols = users.objects.filter(role="volunteer").filter(is_active=True)
    
    # Fetch companies
    comps = users.objects.filter(role="company",is_active=False)
    
    final_vols = []
    final_comps = []


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
        'companys': final_comps
    }
    
    return render(request, 'accept_vol.html', context)

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
    return redirect('/admincustom/acceptusers')
    
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
            <h1 style="text-align:center">Payment Confirmation</h1>
            <p>
            Dear Participant,
            </p>
            <p>
                We are pleased to inform you that we have successfully sent your payment of <strong>{amount}</strong> for attending and participating in the {name}.
            </p>
            <p>
            Thank you for your active participation and contribution to making the event a success. We hope you had a valuable and enjoyable experience.
            </p>
            <p>
            If you have any questions or need further assistance, please do not hesitate to contact us.
            </p>
            <p>
            We look forward to your continued participation in our future events.
            </p>
            <p>Best regards,<br>Any Time Event</p>
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


