# from.views import *
# from django.urls import path

# urlpatterns = [
#     path('acceptusers/' , accept_user , name='accept'),
#     path('pay/' , pay ,name='pay'),
#     path('acceptyes/<volemail>',acceptyes,name="accept_user"),
#     path('acceptno/<volemail>',acceptno,name="reject_user")
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('acceptusers/', views.accept_user, name='accept'),
    path('pay/', views.pay, name='pay'),
    path('acceptyes/<str:volemail>/', views.acceptyes, name="accept_user"),
    path('acceptno/<str:volemail>/', views.acceptno, name="reject_user"),
    path('payvol/<str:event_id>/' , views.payvol , name='payvolenteer' ),
    path('delete/<email>/<role>/',views.delete,name="delete")
]