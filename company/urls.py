from.views import *
from django.urls import path 

urlpatterns = [
    path('',company_home,name='company_home'),
    path('add_event', add_event,name='add_event'),
    path('events/<event_id>/', getevent , name= 'getevent'),
    path('events/',getallevents,name='getallevents'),
    path('get_volunteers/<event_id>/',gettotalvol,name='gettotalvol'),
    path('profile/<id>/',profile,name="profile_comp"),
    path('editprofile/<comp_id>' , editcompany , name = 'editcompany'),
    path('payment/<event_id>/' , getpayment ,name='payment_get' ),
    path('editevent/<event_id1>',editevent,name="editevent"),
    path('present/<event_id>/<email>',markattendenceyes,name="present"),
    path('absent/<event_id>/<email>',markattendenceno,name="absent"),
    path('storedetails',storedetails,name="storedeatail"),
    path('transaction_history/<comp_id>', payment_history , name = 'history'),
    path('payment_success',payment_success,name='payment_success'),
]
