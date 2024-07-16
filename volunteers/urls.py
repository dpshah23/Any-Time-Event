from.views import *
from django.urls import path

urlpatterns = [
    path('',volunteer_home,name='volunteer_home'),
    path('apply/<event_id>',apply,name="applyvol"),
    path('apply/',applyerr,name="applyerr"),
    path('events/',dispevents,name='dispevents'),
    path('profile/<id>/',profile,name="profile_vol"),
    path('editprofile/<vol_id>/',editvol,name="editvol"),
    path('events/<id>',getevent,name='geteventvol'),
    path('unregister/<event_id>',unregister,name="unregister"),
]
