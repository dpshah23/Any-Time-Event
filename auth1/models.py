from django.db import models


# Create your models here.
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
    usage=models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
class company(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=200)
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
    password=models.CharField(max_length=200)
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
    key=models.TextField()
    def __str__(self):
        return self.name