from django.db import models

# Create your models here.
class users(models.Model):
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=200)
    key=models.TextField()
    role=models.Choices('company','volunteer')

    def __str__(self):
        return self.email
    