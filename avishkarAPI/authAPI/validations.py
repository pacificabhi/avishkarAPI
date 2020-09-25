import re, requests, json
from django.contrib.auth.models import User

import secrets
from django.core.mail import send_mail, EmailMessage
from django.conf import settings


#proxies = {'http': 'http://edcguest:edcguest@172.31.102.29:3128','https': 'https://edcguest:edcguest@172.31.102.29:3128','ftp': 'ftp://edcguest:edcguest@172.31.102.29:3128'}
proxies=None


def check_email_dns(email):
	#return True

	url = "https://community-neutrino-email-validate.p.rapidapi.com/email-validate"

	payload = "email=" + email
	headers = {
		'x-rapidapi-host': "community-neutrino-email-validate.p.rapidapi.com",
		'x-rapidapi-key': "8b5a338ae0msh1bd0ef0295a3fd4p128753jsnedc265ba43d9",
		'content-type': "application/x-www-form-urlencoded"
		}

	response = requests.request("POST", url, data=payload, headers=headers)
	
	#print(response.text)

	j=json.loads(response.content.decode('ascii'))
	#print(j)
	if "valid" in j.keys() and j["valid"]:
		return True
	return False



def invalid_name(first_name, last_name):
	pattern=r'[^a-zA-Z ]'
	if(re.search(pattern, first_name) or re.search(pattern, last_name)):
		return "Invalid Name, Only (A-Z) is allowed, No spaces allowed"
	return False


def validate_username(email):
	pattern=r'^[a-z_]{1}[a-z0-9_]{5,}$'
	if(re.match(pattern,email)):
		return True
	return False

def user_exists(username):
	if '@' in username:
		usr=User.objects.filter(email=username)
	else:
		usr=User.objects.filter(username=username)

	if usr:
		return True

	return False

def get_user(username):
	if '@' in username:
		usr=User.objects.filter(email=username)
	else:
		usr=User.objects.filter(username=username)

	if usr:
		return usr.first()

	return None

def validate_password(password):
	if(len(password)<8):
		return False
	return True


def is_valid_number(text):

	try:
		if text[0] == '+':
			text = text[1:]
		int(text)
		return True
	except ValueError:
		return False


def send_info_mail(user, subject, message):

	email_from = settings.EMAIL_HOST_USER
	recipient_list = [user.email,]

	msg = EmailMessage(subject=subject, body=message, from_email=email_from, to=recipient_list)
	msg.content_subtype = "html"  # Main content is now text/html
	res = msg.send()
	
	return res



def send_password_reset_mail(user):

	subject = 'Password Reset'
	new_pass = secrets.token_urlsafe(15)
	
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [user.email,]
	user.userdetails.temp_pass_value = new_pass
	user.userdetails.temp_pass = True

	message = "You are recieving this mail because you requested for temporary password password.<br><br> Your username is <b>%s</b><br><br>Your Temporary Password is <font color='red'><b>%s</b></font><br><br><b>Note:</b> Please change your password after you log in with this password.<br><br>Thank you"%(user.username, new_pass)

	msg = EmailMessage(subject=subject, body=message, from_email=email_from, to=recipient_list)
	msg.content_subtype = "html"  # Main content is now text/html
	res = msg.send()
	if res:
		user.userdetails.save()
	return res