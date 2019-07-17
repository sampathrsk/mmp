from django.db import models

class newTable(models.Model):
	username = models.CharField(max_length=40)
	email = models.EmailField(max_length=70,blank=True)
	first_name = models.CharField(max_length=40)

# Create your models here.
