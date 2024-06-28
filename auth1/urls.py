from.views import *
from django.urls import path
from .views import *

urlpatterns = [
    path('login', login, name='login'),
    path('validate', validate, name='validate'),
    path('logout', logout, name='logout'),
]
