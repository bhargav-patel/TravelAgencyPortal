from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, related_name='profile')
	mobile = models.CharField(max_length=15)
	address = models.CharField(max_length=100)

	def __str__(self):
		return self.user.username+" | "+self.user.email