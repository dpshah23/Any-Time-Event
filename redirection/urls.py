from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name="index"),
    path('contact-us',contact,name="contact"),
    path('logs-redirect-43782912342243589bxhscdujujmiainduxjea',logs,name="logs"),
    path('get-logs-saef3432546', get_logs, name='get_logs'), 
]
