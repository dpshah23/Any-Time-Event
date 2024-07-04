from django.db import models
import datetime
# Create your models here.
class Event(models.Model):
    company_email = models.CharField(max_length=150 , null=True)
    event_company = models.CharField(max_length=200,null=True)
    event_name = models.CharField(max_length=200)
    event_id = models.CharField(max_length=100,unique=True , default=False)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_end_time = models.TimeField(null=True)
    event_location = models.CharField(max_length=100)
    event_loc_link = models.CharField(max_length=400 , null=True)
    event_city = models.CharField(max_length=100 , null=True)
    event_description = models.TextField(max_length=1000)
    event_skills = models.CharField(max_length=200)
    event_rep = models.CharField(max_length=200 , null=True)
    event_rep_no = models.CharField(max_length=15 , null=True)
    event_vol = models.IntegerField()
    event_completed = models.BooleanField(default=False)
    event_mrp = models.IntegerField(null=True)
    actual_amount = models.IntegerField(null=True)  
    paid_status = models.BooleanField(default=False)     

    def is_expired (self):
        return self.event_date < datetime.date.today()
    
    def is_expired (self):
        return self.event_date < datetime.date.today()
    def __str__(self):
        return self.event_name
    
class RegVol(models.Model):
    company_email = models.CharField(max_length=200,null=True)
    event_id_1= models.CharField(max_length=100,null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100)
    paid_status = models.BooleanField()
    
    def __str__(self):
        return self.name