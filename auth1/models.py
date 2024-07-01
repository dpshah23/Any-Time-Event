from django.db import models
from django.utils import timezone
from datetime import timedelta

class Visit(models.Model):
    page_visited = models.CharField(max_length=255, unique=True)
    visit_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.page_visited} - {self.visit_count}"
    

class users(models.Model):
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=200)
    key=models.TextField()
    role=models.CharField(max_length=20)

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
    
class company(models.Model):
    name=models.CharField(max_length=100,default=None)
    email=models.EmailField(max_length=100,default=None)
    phone1=models.CharField(max_length=100,default=None)
    address=models.TextField(default=None)
    website = models.CharField(max_length=100,default=None) #not 
    phone2=models.CharField(max_length=100,default=None) #not
    image_name = models.CharField(max_length=255,default=None)
    card = models.BinaryField(default=None)
    description = models.TextField(default=None) #not
    image_name1 = models.CharField(max_length=255,default=None)
    logo = models.BinaryField(default=None)
    key=models.TextField(default=None)
    def __str__(self):
        return self.name

class volunteer(models.Model):
    name=models.CharField(max_length=100,default=None)
    email=models.EmailField(max_length=100,default=None)
    phone=models.CharField(max_length=100,default=None)
    dob = models.DateField(default=None)
    timestamp = models.DateTimeField(default=None)
    experience = models.CharField(max_length=200,default=None) #not
    skills = models.CharField(max_length=200,default=None) #not 
    qualification = models.CharField(max_length=100,default=None) #dropdown menu
    upi = models.CharField(max_length=100,default=None)
    emergency_contact = models.CharField(max_length=100,default=None)
    image_name = models.CharField(max_length=255,default=None)
    profile_pic = models.BinaryField(default=None)
    image_name1 = models.CharField(max_length=255,default=None)
    card = models.BinaryField(default=None)
    description = models.TextField(default=None)

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