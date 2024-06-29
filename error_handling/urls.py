from django.conf.urls import handler400,handler403,handler404,handler500
from django.urls import path

from .views import *

handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error


urlpatterns = [

]