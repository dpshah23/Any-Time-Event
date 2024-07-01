from django.db import models
from django.utils import timezone

class Visit(models.Model):
    page_visited = models.CharField(max_length=255, unique=True)
    visit_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.page_visited} - {self.visit_count}"
    

class users(models.Model):
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=200)
    key=models.TextField()
    role=models.Choices('company','volunteer')

    def __str__(self):
        return self.email
    
class otps(models.Model):
    email=models.EmailField(max_length=100)
    otp=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return self.email
    
class company(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone1=models.CharField(max_length=100)
    address=models.TextField()
    website = models.CharField(max_length=100) #not 
    phone2=models.CharField(max_length=100) #not
    card = models.ImageField()
    description = models.TextField() #not
    logo = models.ImageField()
    key=models.TextField()
    def __str__(self):
        return self.name

class volunteer(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.CharField(max_length=100)
    dob = models.DateField()
    timestamp = models.DateTimeField()
    experience = models.CharField(max_length=200) #not
    skills = models.CharField(max_length=200) #not 
    qualification = models.CharField(max_length=100) #dropdown menu
    upi = models.CharField(max_length=100)
    emergency_contact = models.CharField(max_length=100)
    profile_pic = models.ImageField()
    card = models.ImageField()
    description = models.TextField()

    def __str__(self):
        return self.name
    

class resetpass(models.Model):
    email=models.EmailField(max_length=100)
    keys=models.TextField()
    usage=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return self.email