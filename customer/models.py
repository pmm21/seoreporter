from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CustomerModel(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	status = models.IntegerField(default = 0)
	credit = models.IntegerField(default = 0)