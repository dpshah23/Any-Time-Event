from django.db import models

# Create your models here.
class payout(models.Model):
    timestamp1 = models.DateField(default=None,null=True)
    vol_id = models.CharField(max_length=100)
    vol_email = models.CharField(max_length=100)
    event_id = models.CharField(max_length=100)
    rz_id = models.TextField()
    entity = models.TextField()
    amount = models.TextField()
    mode = models.TextField()

    def __str__(self):
        return self.vol_id
    