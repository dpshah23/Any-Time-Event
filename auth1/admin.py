from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(users)
admin.site.register(otps)
admin.site.register(company)
admin.site.register(volunteer)
admin.site.register(resetpass)