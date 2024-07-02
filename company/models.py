from django.db import models

# Create your models here.
class event(models.Model):
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=100)
    event_description = models.TextField(max_length=1000)
    event_skills = models.CharField(max_length=200)
    security_deposite = models.IntegerField()
    event_vol = models.IntegerField()
    
    def __str__(self):
        return self.event_name
    
class reg_vol(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    event = models.ForeignKey(event, on_delete=models.CASCADE)
    paid_status = models.BooleanField()
    
    def __str__(self):
        return self.name