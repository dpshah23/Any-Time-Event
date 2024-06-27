from.views import *
from django.urls import path
from .views import *

urlpatterns = [
    path('login', index, name='login'),
]
