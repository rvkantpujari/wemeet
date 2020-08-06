from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):
	email = models.OneToOneField(User,
		on_delete=models.CASCADE, primary_key=True)
	dob = models.DateField(null=True)
	gender = models.CharField(max_length=20, null=True, blank=True)
	mobile = models.IntegerField(null=True)
	alternateEmail = models.EmailField(null=True)
	isVerified = models.BooleanField(default=0)
	profilePic = models.CharField(max_length=1000, null=True)


