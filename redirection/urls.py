from django.urls import path
from .views import *
from volunteers.views import *

urlpatterns = [

    path('',index,name="index"),
    path('contact-us',contact,name="contact"),
    path('logs-redirect-43782912342243589bxhscdujujmiainduxjea',logs,name="logs"),
    path('get-logs-saef3432546', get_logs, name='get_logs'), 
    path('services/',services,name="service"), 
    path('review/',reviews,name="reviews"),
    path('privacy_policy/',privacy_policy,name="privacy"),
    path('our-team/',ourteam,name="ourteam"),
    path('terms-and-condition/',termsandcond,name="termsandcond"),
    path('about-us/',aboutus,name="about"),
    path('transaction_history/' , history , name = 'history'),

]
