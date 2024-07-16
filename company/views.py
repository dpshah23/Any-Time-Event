from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
from django_ratelimit.decorators import ratelimit
from auth1.models import company
from .models import *
import random , string
from django.contrib import messages
from datetime import timedelta
import razorpay
import os 
from dotenv import load_dotenv
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64
from redirection.models import review
import json 
import hashlib 
import  hmac
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@ratelimit(key='ip', rate='5/m')
def company_home(request):
    return HttpResponse("Welcome to Company Home Page")


"""
Function: add_event(request)
----------------------------

Description:
    This function handles the creation and addition of new events by company users. It ensures that the user
    is authenticated and authorized to add events. It gathers event details from the POST request, generates
    a unique event ID, calculates the actual amount after a 25% deduction, saves the event details to the database,
    and sends notification emails to registered volunteers about the new event.

Parameters:
    request (HttpRequest): The HTTP request object containing session data and POST data.

Returns:
    HttpResponse: Returns an appropriate HTTP response based on the process result.
                  - Redirects to '/' with an error message if the user is not logged in.
                  - Redirects to '/' with an error message if the user is a volunteer.
                  - Redirects to '/company/' with a success message upon successful event creation.
                  - Renders 'add_events.html' if the request method is not POST.

Usage:
    This function is typically used in a Django view to handle event creation by company users.
"""
@ratelimit(key='ip', rate='5/m')
def add_event(request):
    # print(request.session['role'])
    # print(request.session['email'])
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    if request.session['role']== "volunteer":
        messages.error(request,"You are not authorized to view this page")
        return redirect('/')
    if request.method == 'POST':
        email = request.session['email']
        event_company = company.objects.get(email=email).name
        comp_id = company.objects.get(email=email).comp_id
        event_name = request.POST.get('eventName')
        alphanumeric_characters = string.ascii_letters + string.digits
        event_id = ''.join(random.choice(alphanumeric_characters) for _ in range(10))
        event_date = request.POST.get('date')
        event_time = request.POST.get('time')
        event_end_time = request.POST.get('etime')
        event_location = request.POST.get('location')
        event_loc_link = request.POST.get('location_link')
        event_city = request.POST.get('event_city')
        event_description = request.POST.get('eventDescription')
        event_skills = request.POST.get('skills_needed')
        event_rep = request.POST.get('companyRep')
        event_rep_no = request.POST.get('contactNo')
        event_vol = request.POST.get('requiredVolunteers')
        event_mrp = request.POST.get('ratePerPerson')
        # event_completed =
        actual_amount = int(event_mrp) - ((int(event_mrp) * 25)/100)
        print(actual_amount)
        event1 = Event(company_email = email ,company_id=comp_id , event_id=event_id,event_company=event_company,event_name=event_name,event_date=event_date,event_time=event_time,event_end_time=event_end_time,event_location=event_location,event_loc_link=event_loc_link,event_city=event_city.lower(),event_description=event_description,event_skills=event_skills,event_rep=event_rep,event_rep_no=event_rep_no,event_mrp=event_mrp,event_vol=event_vol,actual_amount=actual_amount)
        event1.save()
    
        events=Event.objects.filter(company_email=email)
        vollist=[]
        load_dotenv()
        from_email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD1')
        for event in events:
            try:
                emailids = RegVol.objects.filter(event_id_1=event.event_id).values_list('email', flat=True)
                vollist.extend(emailids)
            except Exception as e:
                print(e)
                pass
        
        # Remove duplicates from the volunteer list
        vollist = list(set(vollist))
        
        smtp_server = 'smtp.gmail.com'
        port = 587

        subject=f"New Event Alert from {event_company}"

        registration_link=f"http://127.0.0.1:8000/volunteer/events/{event_id}"

        body=f"""
        
        <div style="font-family: Arial, sans-serif; color: #333;">
    <h1 style="text-align:center; color: #4CAF50;">New Event Alert</h1>
    
    <p>Dear Volunteer,</p>
    
    <p>We are thrilled to inform you that <strong>{event_company}</strong>, with whom you previously registered for an event, is organizing another exciting event!</p>
    
    <p><strong>Event Details:</strong><br>
    <strong>Event Name:</strong> {event_name}<br>
    <strong>Date:</strong> {event_date}<br>
    <strong>Location:</strong> {event_location}</p>
    
    <p>We would love for you to participate in this new event. Your dedication and enthusiasm make a significant difference, and we hope to see you there!</p>
    
    <p style="text-align:center">
        <a href="{registration_link}" style="display:inline-block;padding:10px 20px;margin:10px;color:white;background-color:#4CAF50;border-radius:5px;text-decoration:none;">Register Now</a>
    </p>
    
    <p>If you have any questions or need further assistance, please do not hesitate to contact us.</p>
    
    <p>We look forward to your continued participation and support.</p>
    
    <p>Best regards,<br><strong>The Any Time Event Team</strong></p>
</div>
        """
        bulkmail(smtp_server, port, from_email, password, subject,body, vollist)
        messages.success(request,"Event Added Successfully")
        return redirect('/company/events/')
        
    return render(request,"add_events.html")

"""
Function: getevent(request, event_id)
-------------------------------------

Description:
    This function handles the retrieval and display of event details for a specific event ID. It ensures
    that the user is authenticated and authorized to view the event details. It fetches the event details
    from the database based on the event ID and the logged-in user's email, and renders the event details
    in the 'events.html' template.

Parameters:
    request (HttpRequest): The HTTP request object containing session data.
    event_id (str): The unique identifier of the event to be retrieved.

Returns:
    HttpResponse: Returns an appropriate HTTP response based on the process result.
                  - Redirects to '/' with an error message if the user is not logged in.
                  - Redirects to '/' with an error message if the user is a volunteer.
                  - Redirects to '/company/' with an error message if the event is not found.
                  - Renders 'events.html' with the event details if the event is found.

Usage:
    This function is typically used in a Django view to display event details for a specific event ID
    to the authorized company users.
"""
@ratelimit(key='ip', rate='5/m')
def getevent(request,event_id):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    if request.session['role']== "volunteer":   
        messages.error(request,"You are not authorized to view this page")
        return redirect('/')
    try:
        email=request.session['email']
        events=Event.objects.get(event_id=event_id,company_email=email)
        # num_vol = reg_vol.objects.get(event_id=event_id)
        # print(num_vol)
    except Event.DoesNotExist:
        messages.error(request,"Event Not Found")
        return redirect('/company/')
    event1 = events.is_expired
    return render (request , "events.html",{'event':events , 'event1' : event1})


"""
Function: getallevents(request)
------------------------------

Description:
    This function retrieves and displays all events associated with the logged-in company user. It ensures
    that the user is authenticated and authorized to view the events. It filters the events based on the
    user's email, separates expired and active events, and renders them in the 'all_events.html' template.

Parameters:
    request (HttpRequest): The HTTP request object containing session data.

Returns:
    HttpResponse: Returns an appropriate HTTP response based on the process result.
                  - Redirects to '/' with an error message if the user is not logged in.
                  - Redirects to '/' with an error message if the user is a volunteer.
                  - Renders 'all_events.html' with the expired and active events if the user is authorized.

Usage:
    This function is typically used in a Django view to display all events for the logged-in company user,
    categorizing them as expired or active events.
"""
@ratelimit(key='ip', rate='5/m')
def getallevents(request):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    if request.session['role']== "volunteer":
        messages.error(request,"You are not authorized to view this page")
        return redirect('/')
    
    email=request.session['email']
    all_events = Event.objects.filter(company_email=email)
    events_expired = [event for event in all_events if event.is_expired()]  
    events_active = [event for event in all_events if not event.is_expired()]

    required=0
    total_events_no=len(events_expired  )
    activeno=len(events_active)
    for event in all_events:
        required+=event.event_vol

    total=len(RegVol.objects.filter(company_email=email))

    print(required,total)

    
    return render(request,"all_events.html",{'events_ex':events_expired,'events':events_active,'num_active':activeno,'company_name':company.objects.get(email=email).name , 'obj' : company.objects.get (email = email),'required':required,'total':total,'total_events_no':total_events_no})

"""
Function: gettotalvol(request, event_id)
---------------------------------------

Description:
    This function retrieves and displays the list of volunteers registered for a specific event. It ensures
    that the user is authenticated and authorized to view the volunteer list. It fetches the event and the
    associated volunteers from the database based on the event ID and the logged-in user's email, and renders
    the list of volunteers in the 'list_of_attendees.html' template.

Parameters:
    request (HttpRequest): The HTTP request object containing session data.
    event_id (str): The unique identifier of the event for which the volunteer list is to be retrieved.

Returns:
    HttpResponse: Returns an appropriate HTTP response based on the process result.
                  - Redirects to '/' with an error message if the user is not logged in.
                  - Redirects to '/' with an error message if the user is a volunteer.
                  - Renders 'list_of_attendees.html' with the event and volunteer details if the event is found.
                  - Redirects to '/company/' with an error message if the event or volunteers are not found.

Usage:
    This function is typically used in a Django view to display the list of volunteers for a specific event
    to the authorized company users.
"""
@ratelimit(key='ip', rate='10/m')
def gettotalvol(request,event_id):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    if request.session['role']== "volunteer":
        messages.error(request,"You are not authorized to view this page")
        return redirect('/')
    email=request.session['email']
    # events = Event.objects.filter(company_email=email,event_id=event_id)
    try:
        events = Event.objects.get(company_email=email,event_id=event_id)
        volunteers = RegVol.objects.filter(event_id_1=event_id)

        return render(request,"list_of_attendes.html",{'event':events,'volunteers':volunteers,'length':len(volunteers)})

    except Event.DoesNotExist:
        messages.error(request,"Event Not Found")
        return redirect('/company/')
    except RegVol.DoesNotExist:
        messages.error(request,"No Volunteers Registered")
        return redirect('/company/')


"""
Function: profile(request, id)
------------------------------

Description:
    This function handles the retrieval and display of a company's profile information based on the provided
    company ID. It ensures that the user is authenticated and authorized to view the profile. It fetches the
    company's details from the database and renders them in the 'profile.html' template.

Parameters:
    request (HttpRequest): The HTTP request object containing session data.
    id (str): The unique identifier of the company whose profile is to be retrieved.

Returns:
    HttpResponse: Returns an appropriate HTTP response based on the process result.
                  - Redirects to '/' with an error message if the user is not logged in.
                  - Displays an error message if the user is a volunteer.
                  - Displays an error message if the user does not have permission to view the profile.
                  - Renders 'profile.html' with the company details if the user is authorized.
                  - Redirects to '/company/' with an error message if the company is not found.

Usage:
    This function is typically used in a Django view to display the profile of a company to authorized users.
"""
@ratelimit(key='ip',rate='10/m')
def profile(request,id):
    # print(id)
    # print('in profile')
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    
    try:
        email = company.objects.get(comp_id = id ).email
        obj=company.objects.get(comp_id=id)
        # if obj.email!=request.session['email']:
        #     messages.error(request,"You Don't have permission to view this page")
        print(obj)
    except Exception as e:
        print("error")
        messages.error(request,"Company Not Found")
        return redirect('/company/')
    
    return render(request,"profile_company.html",{'data':obj , 'company':email})
    

"""
Function: getpayment(request, event_id)
--------------------------------------

Description:
    This function handles the payment process for a specific event using the Razorpay API. It calculates the total
    payment amount based on the number of volunteers who attended the event and the event's rate per person.
    It creates a payment order with Razorpay, updates the event's payment status, and saves the payment information
    in the database.

Parameters:
    request (HttpRequest): The HTTP request object containing session data.
    event_id (str): The unique identifier of the event for which the payment is to be processed.

Returns:
    HttpResponse: Returns an appropriate HTTP response based on the process result.
                  - Renders 'payment.html' with the payment details if the payment order is successfully created.

Usage:
    This function is typically used in a Django view to process payments for a specific event and update the
    payment status in the database.
"""
@ratelimit(key='ip',rate='5/m')
# def getpayment(request, event_id):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         feedbackreview = request.POST.get('feedback')
#         date1 = date.today()

#         print(name, email, feedbackreview, date1)

#         review_obj = review(name=name, email=email, review=feedbackreview, date=date1)
#         review_obj.save()
#         try:
#             ispaid1 = Event.objects.get(event_id=event_id).paid_status
#         except Event.DoesNotExist:
#             messages.error(request, "Event Not Found")
#             return redirect('/company/events/')
        
#         messages.success(request, "Review Added Successfully")

#         if ispaid1:
#             return redirect('/company/events/')
    
#     load_dotenv()
#     key = os.getenv('api_key_razorpay')
#     secret = os.getenv('api_secret_razorpay')
#     client = razorpay.Client(auth=(key, secret))

#     total_vol = len(RegVol.objects.filter(event_id_1=event_id, attendence="present"))
#     event = Event.objects.get(event_id=event_id)
#     event_mrp = Event.objects.get(event_id=event_id).event_mrp
#     amount = event_mrp * total_vol
#     final_amt = int(amount) * 100  # Razorpay amount is in paise

#     ispaid = event.paid_status

#     if ispaid:
#         messages.error(request, "Payment Already Done")
#         return render(request, "payment.html", {'ispaid': ispaid, 'event_id': event_id})

#     try:
#         payment = client.order.create({"amount": final_amt, "currency": "INR", "payment_capture": '1'})
#     except Exception as e:
#         print("Error creating order: ", e)
#         return render(request, "error.html", {"message": "Error creating Razorpay order"})

#     print(payment)
#     timestamp = date.today()
#     payment_id = payment['id']
#     company_email = event.company_email
#     company_id = company.objects.get(email=company_email).comp_id
#     event_name = event.event_name
#     event_date = event.event_date

#     pay = company_payment(timestamp=timestamp, event_id=event_id, event_name=event_name, event_date=event_date, amount=amount, order_id=payment_id, company_id=company_id)
#     pay.save()

#     return render(request, "payment.html", {'payment': payment, 'key': key, 'event_id': event_id, 'ispaid': ispaid})
def getpayment(request, event_id):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        feedbackreview = request.POST.get('feedback')
        date1 = date.today()

        print(name, email, feedbackreview, date1)

        review_obj = review(name=name, email=email, review=feedbackreview, date=date1)
        review_obj.save()
        try:
            ispaid1 = Event.objects.get(event_id=event_id).paid_status
        except Event.DoesNotExist:
            messages.error(request, "Event Not Found")
            return redirect('/company/events/')
        
        messages.success(request, "Review Added Successfully")

        if ispaid1:
            return redirect('/company/events/')
    
    load_dotenv()
    key = os.getenv('api_key_razorpay')
    secret = os.getenv('api_secret_razorpay')
    client = razorpay.Client(auth=(key, secret))

    total_vol = len(RegVol.objects.filter(event_id_1=event_id, attendence="present"))
    event = Event.objects.get(event_id=event_id)
    event_mrp = Event.objects.get(event_id=event_id).event_mrp
    amount = event_mrp * total_vol
    final_amt = int(amount) * 100

    ispaid = event.paid_status

    if ispaid:
        messages.error(request, "Payment Already Done")
        return render(request, "payment.html", {'ispaid': ispaid, 'event_id': event_id})

    try:
        payment = client.order.create({"amount": final_amt, "currency": "INR", "payment_capture": '1'})
    except Exception as e:
        print("Error creating order: ", e)
        return render(request, "error.html", {"message": "Error creating Razorpay order"})

    print(payment)
    timestamp = date.today()
    payment_id = payment['id']
    company_email = event.company_email
    company_id = company.objects.get(email=company_email).comp_id
    event_name = event.event_name
    event_date = event.event_date

    pay = company_payment(timestamp=timestamp, event_id=event_id, event_name=event_name, event_date=event_date, amount=amount, order_id=payment_id, company_id=company_id)
    pay.save()

    return render(request, "payment.html", {'payment': payment, 'key': key, 'event_id': event_id, 'ispaid': ispaid})


    
"""
Function: editevent(request, event_id1)
--------------------------------------

Description:
    This function handles the editing of event details for a specific event. It ensures that the user is authenticated
    and authorized to edit the event. It retrieves the event details from the database, updates them based on the 
    POST data from the request, and saves the updated event details.

Parameters:
    request (HttpRequest): The HTTP request object containing session data.
    event_id1 (str): The unique identifier of the event to be edited.

Returns:
    HttpResponse: Returns an appropriate HTTP response based on the process result.
                  - Redirects to '/' with an error message if the user is not logged in.
                  - Displays an error message if the user is a volunteer.
                  - Redirects to '/company/events/' with a success message if the event details are successfully updated.
                  - Redirects to '/company/' with an error message if the event does not exist.
                  - Redirects to '/' if any other exception occurs.
                  - Renders 'edit_event.html' with the event details if the request method is GET.

Usage:
    This function is typically used in a Django view to allow authorized users to edit the details of a specific event.
"""
@ratelimit(key='ip',rate='5/m')
def editevent(request,event_id1):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    
    if request.session['role']=="volunteer":
        messages.error(request,"You Don't have permission to view this page")

    try:
        email=request.session['email']
        # if request.sess
        event=Event.objects.get(event_id=event_id1,company_email=email)

        if request.method=="POST":
            email = request.session['email']
            event_company = company.objects.get(email=email).name
            event_name = request.POST.get('eventName')
            event_date = request.POST.get('date')
            event_time = request.POST.get('time')
            event_end_time = request.POST.get('etime')
            event_location = request.POST.get('location')
            event_loc_link = request.POST.get('location_link')
            event_city = request.POST.get('event_city')
            event_description = request.POST.get('eventDescription')
            event_skills = request.POST.get('skills_needed')
            event_rep = request.POST.get('companyRep')
            event_rep_no = request.POST.get('contactNo')
            event_vol = request.POST.get('requiredVolunteers')
            event_mrp = request.POST.get('ratePerPerson')
            actual_amount = int(event_mrp) - ((int(event_mrp) * 25)/100)
            obj, created = Event.objects.update_or_create(
                event_id=event_id1,
                defaults={
                    'event_name':event_name,
                    'event_date':event_date,
                    'event_time':event_time,
                    'event_end_time':event_end_time,
                    'event_location':event_location,
                    'event_loc_link':event_loc_link,
                    'event_city':event_city.lower(),
                    'event_description':event_description,
                    'event_skills':event_skills,
                    'event_rep':event_rep,
                    'event_rep_no':event_rep_no,
                    'event_mrp':event_mrp,
                    'event_vol':event_vol,
                    'actual_amount':actual_amount,
                }
            )
            

            print("Updated")
            messages.success(request,'Event Details Updated Successfully')
            return redirect('/company/events/')
    except Event.DoesNotExist:
        messages.error('Event Does Not Exists')
        return redirect('/company/events/')
    except Exception as e:
        print(e)
        return redirect('/')

    return render(request,'edit_event.html',{'event':event})


"""
Function: markattendenceyes(request, event_id, email)
----------------------------------------------------

Description:
    This function marks the attendance of a volunteer as present for a specific event. It retrieves the
    volunteer's registration record based on the event ID and email, updates the attendance status to True,
    saves the changes, and redirects to the list of volunteers for that event.

Parameters:
    request (HttpRequest): The HTTP request object containing session data.
    event_id (str): The unique identifier of the event.
    email (str): The email address of the volunteer whose attendance is to be marked as present.

Returns:
    HttpResponse: Redirects to the list of volunteers for the specified event with a success message.

Usage:
    This function is typically used in a Django view to allow authorized users to mark the attendance of
    volunteers as present for a specific event.
"""
def markattendenceyes(request,event_id,email):
    obj=RegVol.objects.get(event_id_1=event_id,email=email)
    obj.attendence="present"
    obj.save()
    messages.success(request,"Attendence Marked To Present")
    return redirect(f'/company/get_volunteers/{event_id}')


"""
Function: markattendenceno(request, event_id, email)
---------------------------------------------------

Description:
    This function marks the attendance of a volunteer as absent for a specific event. It retrieves the
    volunteer's registration record based on the event ID and email, updates the attendance status to False,
    saves the changes, and redirects to the list of volunteers for that event.

Parameters:
    request (HttpRequest): The HTTP request object containing session data.
    event_id (str): The unique identifier of the event.
    email (str): The email address of the volunteer whose attendance is to be marked as absent.

Returns:
    HttpResponse: Redirects to the list of volunteers for the specified event with a success message.

Usage:
    This function is typically used in a Django view to allow authorized users to mark the attendance of
    volunteers as absent for a specific event.
"""
def markattendenceno(request,event_id,email):
    obj=RegVol.objects.get(event_id_1=event_id,email=email)
    obj.attendence="absent"
    obj.save()
    messages.success(request,"Attendence Marked To Absent")
    return redirect(f'/company/get_volunteers/{event_id}')

"""
Function: bulkmail(smtp_server, port, sender_email, sender_password, subject, body, recipient_list)
-------------------------------------------------------------------------------------------------

Description:
    This function sends bulk emails to a list of recipients. It connects to the specified SMTP server, 
    logs in with the provided sender email and password, and sends an email with the given subject and 
    body to each recipient in the recipient list.

Parameters:
    smtp_server (str): The SMTP server address (e.g., 'smtp.gmail.com').
    port (int): The port number for the SMTP server (e.g., 587 for TLS).
    sender_email (str): The email address of the sender.
    sender_password (str): The password or app-specific password for the sender's email account.
    subject (str): The subject of the email.
    body (str): The HTML body of the email.
    recipient_list (list): A list of recipient email addresses.

Returns:
    None

Usage:
    This function is typically used to send bulk emails for notifications, newsletters, or announcements
    to a list of recipients.
"""
def bulkmail(smtp_server, port, sender_email, sender_password, subject, body, recipient_list):
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)
        
        for recipient in recipient_list:
            # Create the email headers and body
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))

            # Send the email
            server.sendmail(sender_email, recipient, msg.as_string())
            print(f"Email sent to {recipient}")
    pass
'''
Function Name:
editcompany (request,comp_id)

Description:
This view function allows users to edit the details of an existing company. It checks if the user is logged in and has the necessary permissions. If the user has the required permissions, the function retrieves the company object by its ID and updates its details based on the submitted form data. If a company logo is provided, it validates the file format and encodes it in base64 before saving. After successful updates, the user is redirected to the company's profile page.

Parameters:
request: The HTTP request object containing metadata about the request and user data.
comp_id: The ID of the company to be edited.

Returns:
Redirects to the home page ('/') if the user is not logged in.
Redirects to the same page if the user does not have permission to view the page.
Renders the edit company page with the current company details if the form submission is invalid.
Redirects to the company profile page after successful updates.
Redirects to the company list page if the company does not exist.
Redirects to the home page for any other exceptions.

Usage:
This function is intended to be used in a Django web application as a view for editing company details. 
'''

@ratelimit(key='ip', rate='5/m')
def editcompany(request, comp_id):
    if 'email' not in request.session or 'role' not in request.session:
        messages.error(request, "You are not logged in")
        return redirect('/')

    if request.session['role'] == "volunteer":
        messages.error(request, "You don't have permission to view this page")
        return redirect('/')

    try:
        comp = company.objects.get(comp_id=comp_id)

        if comp.email != request.session['email']:
            messages.error(request, "You don't have permission to view this page")
            return redirect('/')

        if request.method == "POST":
            if 'company_logo' in request.FILES:
                image_file = request.FILES['company_logo']
                valid_extensions = ['jpg', 'png', 'jpeg', 'heic']
                if image_file.name.split('.')[-1].lower() not in valid_extensions:
                    messages.error(request, 'Invalid image format. Only JPG, PNG, JPEG, and HEIC are allowed.')
                    return render(request, 'edit_company.html', {'company': comp})

                image_data = image_file.read()
                comp_logo = base64.b64encode(image_data).decode('utf-8')
            else:
                comp_logo = comp.logo

            name = request.POST.get('name')
            phone1 = request.POST.get('phone1')
            address = request.POST.get('address')
            website = request.POST.get('website')
            phone2 = request.POST.get('phone2')
            description = request.POST.get('description')

            # print(f"Updating company: {comp_id} with data: {name}, {phone1}, {address}, {website}, {phone2}, {description}, {comp_logo}")

            obj, created = company.objects.update_or_create(
                comp_id=comp_id,
                defaults={
                    'name': name,
                    'phone1': phone1,
                    'address': address,
                    'website': website,
                    'phone2': phone2,
                    'description': description,
                    'logo': comp_logo
                }
            )

            messages.success(request, 'Company details updated successfully')
            return redirect(f'/company/profile/{comp_id}')
    except company.DoesNotExist:
        messages.error(request, 'Company does not exist')
        return redirect(f'/company/profile/{comp_id}')
    except Exception as e:
        print(f"Error: {e}")
        messages.error(request, 'An error occurred while updating the company details')
        return redirect('/')

    return render(request, 'edit_company.html', {'company': comp})


'''

Function Name: storedetails

    Handles the verification and storage of payment details received from Razorpay.
    Redirects to appropriate pages based on payment verification status.
    
    Request Method:
        - POST: Accepts JSON data for payment verification.
        - GET: Accepts query parameters for payment verification (not recommended for sensitive data).

    Parameters:
        - order_id: Razorpay order ID.
        - payment_id: Razorpay payment ID.
        - signature: Razorpay payment signature.
        - amount: Amount of payment received (converted from paise to currency).
        - event_id: ID of the event for which payment is being processed.

    Exceptions:
        - SignatureVerificationError: Raised when the payment signature verification fails.
        - Any other exception: Handles general errors that may occur during payment processing.

    Sends an email notification to the event organizer upon successful payment, including event details and payment amount.

    Disclaimer:
        - Includes a disclaimer in the email body stating that any attempt to bypass payment may result in rejection and legal action.

    Redirects:
        - '/company/payment_success': Redirects on successful payment verification.
        - '/company/events': Redirects on payment failure.

'''
def storedetails(request):
 
   
    if request.method == "POST":
        data = json.loads(request.body)
    elif request.method == "GET":
        data = request.GET
    else:
        messages.error(request, "Invalid request method")
        return redirect('/')

    order_id = data.get('order_id')
    payment_id = data.get('payment_id')
    signature = data.get('signature')
    amount = int(data.get('amount'))/100
    event_id = data.get('event_id')

    key = os.getenv('api_key_razorpay')
    secret = os.getenv('api_secret_razorpay')
    client = razorpay.Client(auth=(key, secret))

    print("authorize")

    params_dict = {
        'razorpay_order_id': order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }

    try:
        client.utility.verify_payment_signature(params_dict)

        payment, created = company_payment.objects.update_or_create(
            order_id=order_id,
            defaults={'status': True, 'payment_id': payment_id, 'amount': amount, 'signature': signature}
        )
        if company_payment.objects.filter(event_id=event_id, status=True).exists():
            event, created = Event.objects.update_or_create(
                event_id=event_id,
                defaults={'paid_status': True}
            )

        print("Verified")

        load_dotenv()
        from_email=os.getenv('EMAIL')
        password=os.getenv('PASSWORD1')

        name=Event.objects.get(event_id=event_id).event_name
        total_vol = len(RegVol.objects.filter(event_id_1=event_id, attendence="present"))
        event_mrp = Event.objects.get(event_id=event_id).event_mrp
        amount = event_mrp * total_vol

        email = Event.objects.get(event_id=event_id).company_email

        subject=f"Payment Received for {name}"

        body=f"""
        <div style="font-family: Arial, sans-serif; color: #333;">
        <h1 style="text-align:center; color: #4CAF50;">Payment Received</h1>

        <p>Dear Organizer,</p>
        
        <p>We are pleased to inform you that the payment for the event <strong>{name}</strong> has been successfully received.</p>

        <p><strong>Event Name:</strong> {name}<br>
        <strong>Total Amount:</strong> INR {amount}</p>

        <p>If you have any questions or need further assistance, please do not hesitate to contact us.</p>

        <p>We appreciate your continued support and look forward to working with you on future events.</p>

        <p>Best regards,<br><strong>The Any Time Event Team</strong></p>
        
        <p><em>Note: In case of any discrepancy found during payment, we reserve the right to reject your payment and take legal action against attempts to bypass payment.</em></p>
        </div>
        """

        send_mail('smtp.gmail.com', 587, from_email, password, subject, body,email)
        
        messages.success(request, "Payment Successful")
        return redirect('/company/payment_success')  # Redirect on success
    except razorpay.errors.SignatureVerificationError:

        print("failed")
        messages.error(request, "Payment Failed")
        return redirect('/company/events')  # Redirect on failure
    except Exception as e:
        print(e)
        messages.error(request, "An error occurred")
        return redirect('/')

        messages.success(request,"payment Successful")
        return redirect(f'/company/events')
    
'''
Function Name: payment_history

Description:
This view function displays the payment history for the logged-in company. It checks if the user is logged in and has the appropriate
permissions. If the user has the required permissions, it retrieves the payment history for the company associated with the logged-in user
and renders the transaction.html template with the payment history data.

Parameters:
request: The HTTP request object containing metadata about the request and user data.

Returns:
Redirects to the home page ('/') if the user is not logged in.
Redirects to the same page if the user does not have permission to view the page.
Redirects to the company list page if the company does not exist.
Renders the transaction.html template with the payment history data for the company.

Usage:
This function is intended to be used in a Django web application as a view for displaying the payment history of a company.
'''

@ratelimit(key='ip',rate='5/m')
def payment_history(request , comp_id):
    if 'email' and 'role' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('/')
    
    if request.session['role']=="volunteer":
        messages.error(request,"You Don't have permission to view this page")
    email = request.session['email']
    try :
        history = company_payment.objects.filter(company_id=comp_id)
    
    except company.DoesNotExist:
        messages.error(request,'company Does Not Exists')
        return redirect('/company/')
    except Exception as e:
        print(e)
        return redirect('/')
    
    return render(request ,'transcation.html' , {'history' : history} )
        

def payment_success(request):

    return render(request, 'payment_success.html')


def send_mail(smtp_server, port, sender_email, sender_password, subject, body,recipient):


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

