from.views import *
from django.urls import path 

urlpatterns = [
    path('',company_home,name='company_home'),
    path('add_event', add_event,name='add_event'),
    path('events/<event_name>/', getevent , name= 'getevent')
]
