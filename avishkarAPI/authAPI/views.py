from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .validations import *
from .models import UserDetails

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
				