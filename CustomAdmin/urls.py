from.views import *
from django.urls import path

urlpatterns = [
    path('/acceptusers/' , accept_user , name='accept'),
    path('/pay/' , pay ,name='pay'),
    path('acceptyes/<volemail>',acceptyes,name="accept_user"),
    path('acceptno/<volemail>',acceptno,name="reject_user")
]
