from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .validations import *
from .models import UserDetails

from django.views.decorators.csrf import csrf_exempt

class HelloView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class RegisterUser(APIView):

    
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):
        context = {"success": True, "loggedin": False}
        
        if request.user.is_authenticated:
            context["success"]=False
            context["loggedin"]=True
            token = Token.objects.get_or_create(user=request.user)
            context["token"] = token[0].key
            return Response(context)

        errors = []
        email = request.POST.get("email").strip().lower()
        username = request.POST.get("username").strip().lower()
        password = request.POST.get("password")

        if not validate_username(username):
            errors.append("Invalid Username")
        elif user_exists(username):
            errors.append("Username already taken")

        if user_exists(email):
            errors.append("Email already taken")
        elif not check_email_dns(email):
            errors.append("Invalid Email")

        if not validate_password(password):
            errors.append("Password must be 8 characters long")

        if errors:
            context["success"]=False
            context["errors"]=errors
            return Response(context)

        u = User.objects.create(username = username, email = email)
        u.set_password(password)
        u.save()

        ud = UserDetails.objects.create(user = u)

        token = Token.objects.get_or_create(user=u)
        context["token"] = token[0].key

        return Response(context)
				


class UpdateUserNameAndEmail(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):

        context = {"success": False}
        errors = []

        fname = request.POST.get("fname").strip().title()
        lname = request.POST.get("lname").strip().title()
        email = request.POST.get("email").strip().lower()

        nerr = invalid_name(fname, lname)

        if user_exists(email):
            if email != request.user.email:
                errors.append("Email already taken")
        
        elif not check_email_dns(email):
            errors.append("Invalid Email")

        if nerr:
            errors.append(nerr)

        if errors:
            context["errors"]=errors
            return Response(context)

        request.user.first_name = fname
        request.user.last_name = lname
        request.user.email = email
        request.user.save()
        context["success"] = True
        return Response(context)



class UpdateUserDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):

        context = {"success": False}
        errors = []

        college = request.POST.get("college").strip()
        phone = request.POST.get("phone").strip()
        whatsapp = request.POST.get("whatsapp").strip()
        msteams = request.POST.get("msteams").strip()

        if not is_valid_number(phone):
            errors.append("Invalid Phone Number")

        if not is_valid_number(whatsapp):
            errors.append("Invalid WhatsApp Number")

        if errors:
            context["errors"]=errors
            return Response(context)

        ud = request.user.userdetails
        if not ud.is_fees_paid():
            ud.college = college
        ud.phone = phone
        ud.whatsapp = whatsapp
        ud.msteams_id = msteams

        ud.save()

        context["success"] = True

        return Response(context)



class UpdateFeesStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):

        context = {"success": False}

        status = request.POST.get("status").strip()
        ud = request.user.userdetails
        
        if status == "paid":
            ud.fees_paid = True
            context["message"] = "Fees paid successfully"
        elif status == "pending":
            ud.fees_paid = False
        
        ud.save()
        context["success"] = True

        return Response(context)

        


