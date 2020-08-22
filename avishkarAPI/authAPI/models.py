from django.db import models
from django.contrib.auth.models import User



class UserDetails(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
	confirmed = models.BooleanField(blank=False, null=False, default=False)
	confirm_token = models.CharField(max_length=256 ,blank=True, null=False, default="")
	fees_paid = models.BooleanField(default=False)

	whatsapp = models.CharField(max_length=16, blank=True, null=False, default="")
	phone = models.CharField(max_length=16, blank=True, null=False, default="")
	college = models.TextField(max_length=255, blank=True, null=False, default="")
	msteams_id = models.CharField(max_length=200, blank=True, null = False, default="")

	resume = models.TextField(max_length=5000, blank=True, null=False, default="")
	notifications = models.TextField(max_length=5000, blank=True, null=False, default="")
	

	def __str__(self):
		return self.user.username

	def is_user_confirmed(self):
		return self.confirmed

	def is_fees_paid(self):
		return self.fees_paid

	def get_username(self):
		return self.user.get_username()

	def get_name(self):
		return self.user.get_full_name()

	def get_email(self):
		return self.user.email

	