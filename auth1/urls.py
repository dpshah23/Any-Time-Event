from.views import *
from django.urls import path
from .views import *

urlpatterns = [
    path('login', login, name='login'),
]
urlpatterns = [
    path('signup', signup, name='signup'),
]