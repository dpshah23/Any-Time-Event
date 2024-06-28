from.views import *
from django.urls import path
from .views import *

urlpatterns = [
    path('login', login, name='login'),
    path('validate', validate, name='validate'),
    path('logout', logout, name='logout'),
    path('volunteerinfo', volunteerinfo, name='volunteerinfo'),
    path('companyinfo', companyinfo, name='companyinfo'),
    path('signup', signup, name='signup'),
    path('reset', reset, name='reset'),
    path('resetpass', resetpass, name='resetpass'),
]
