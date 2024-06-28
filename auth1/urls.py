from.views import *
from django.urls import path
from .views import *

urlpatterns = [
    path('login', login, name='login'),
    path('validate', validate, name='validate'),
    path('logout', logout, name='logout'),
]
urlpatterns = [
    path('signup', signup, name='signup'),
]
urlpatterns = [
    path('companyinfo', companyinfo, name='companyinfo'),
]
urlpatterns = [
    path('volunteerinfo', volunteerinfo, name='volunteerinfo'),
]