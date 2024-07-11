from django.db import models

# Create your models here.
class contactus(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    message=models.TextField()

    def __str__(self):
        return self.name
    
class review(models.Model):
    name=models.CharField(max_length=150)
    email=models.EmailField(max_length=250)
    review=models.TextField()

    def __str__(self):
        return self.name