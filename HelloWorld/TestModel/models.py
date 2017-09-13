from django.db import models

# Create your models here.
# models.py

 
class Test(models.Model):
    name = models.CharField(max_length=20)
