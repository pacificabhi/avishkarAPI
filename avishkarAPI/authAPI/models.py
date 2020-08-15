from django.db import models
from django.contrib.auth.models import User



class UserDetails(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
	confirmed = models.BooleanField(blank=False, null=False, default=False)
	confirm_token = models.CharField(max_length=256 ,blank=True, null=False, default="")
	

	def __str__(self):
		return self.user.username

	def is_account_confirmed(self):
	
		return self.confirmed