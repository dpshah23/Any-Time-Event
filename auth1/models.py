from django.db import models
from django.utils import timezone
from datetime import timedelta
import datetime

class Visit(models.Model):
    page_visited = models.CharField(max_length=255, unique=True)
    visit_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.page_visited} - {self.visit_count}"
    

class users(models.Model):
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=200)
    key=models.TextField()
    role=models.CharField(max_length=20,default=None)
    is_active = models.BooleanField(default=False,null=True)
    timestamp = models.DateField(default=None, null=True)
    
    def is_expired(self):
         return self.timestamp < datetime.date.today()
        
    def __str__(self):
        return self.email
    
class otps(models.Model):
    email=models.EmailField(max_length=100)
    otp=models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(minutes=5))

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return self.email
    
# class company(models.Model):
#     name=models.CharField(max_length=100,default=None)
#     email=models.EmailField(max_length=100,default=None)
#     phone1=models.CharField(max_length=100,default=None)
#     address=models.TextField(default=None)
#     website = models.CharField(max_length=100,default=None) #not 
#     phone2=models.CharField(max_length=100,default=None) #not
#     image_name = models.CharField(max_length=255,default=None)
#     card = models.BinaryField(default=None)
#     description = models.TextField(default=None) #not
#     image_name1 = models.CharField(max_length=255,default=None)
#     logo = models.BinaryField(default=None)
#     key=models.TextField(default=None)
#     def __str__(self):
#         return self.name

# class volunteer(models.Model):
#     name=models.CharField(max_length=100,default=None)
#     email=models.EmailField(max_length=100,default=None)
#     phone=models.CharField(max_length=100,default=None)
#     dob = models.CharField(max_length=150,default=None)
#     timestamp = models.CharField(max_length=250,default=None)
#     experience = models.CharField(max_length=200,default=None) #not
#     skills = models.CharField(max_length=200,default=None) #not 
#     qualification = models.CharField(max_length=100,default=None) #dropdown menu
#     upi = models.CharField(max_length=100,default=None)
#     emergency_contact = models.CharField(max_length=100,default=None)
#     image_name = models.CharField(max_length=255,default=None)
#     profile_pic = models.BinaryField(default=None)
#     image_name1 = models.CharField(max_length=255,default=None)
#     card = models.BinaryField(default=None)
#     description = models.TextField(default=None)

#     def __str__(self):
#         return self.name
    


class company(models.Model):
    comp_id=models.CharField(max_length=100, default=None, null=True)
    name = models.CharField(max_length=100, default=None, null=True)
    email = models.EmailField(max_length=100, default=None)
    phone1 = models.CharField(max_length=100, default=None, null=True)
    address = models.TextField(default=None, null=True)
    website = models.CharField(max_length=100, default=None, null=True)
    phone2 = models.CharField(max_length=100, default=None, null=True)
    image_name = models.CharField(max_length=255, default=None, null=True)
    card = models.TextField(default=None, null=True)
    description = models.TextField(default=None, null=True)
    image_name1 = models.CharField(max_length=255, default=None, null=True)
    logo = models.TextField(default=None, null=True)
    key = models.TextField(default=None, null=True)

    def __str__(self):
        return self.name

class volunteer(models.Model):
    vol_id=models.CharField(max_length=100, default=None, null=True)
    name = models.CharField(max_length=100, default=None, null=True)
    email = models.EmailField(max_length=100, default=None, null=True)
    phone = models.CharField(max_length=100, default=None, null=True)
    dob = models.CharField(max_length=150, default=None, null=True)
    experience = models.CharField(max_length=200, default=None, null=True)
    skills = models.CharField(max_length=200, default=None, null=True)
    qualification = models.CharField(max_length=100, default=None, null=True)
    upi = models.CharField(max_length=100, default=None, null=True)
    emergency_contact = models.CharField(max_length=100, default=None, null=True)
    image_name = models.CharField(max_length=255, default=None,null=True)
    profile_pic = models.TextField(default=None, null=True)
    image_name1 = models.CharField(max_length=255, default=None, null=True)
    card = models.TextField(default=None, null=True)
    description = models.TextField(default=None, null=True)
    contact_id = models.CharField(max_length=200 , null=True)
    fund_id = models.CharField(max_length=200 , null=True)
    city = models.CharField(max_length=100 , null=True)

    def __str__(self):
        return self.name

class resetpass(models.Model):
    email=models.EmailField(max_length=100)
    keys=models.TextField()
    usage=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(hours=1))

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return self.email