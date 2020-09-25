from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .validations import *
from .models import UserDetails
from events.models import EventTeam,Event

from django.contrib.auth import authenticate

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
        is_mnnit = request.POST.get("ismnnit")

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
        if is_mnnit == "true" or is_mnnit == "True":
            ud.college = "MNNIT"
            ud.fees_paid = True
            ud.save()

        token = Token.objects.get_or_create(user=u)
        context["token"] = token[0].key

        info_msg = "You are successfully registered for Avishkar 2020. Your username is <span style='color: green; font-weight:bold;'>{}</span> and password is <span style='color: red; font-weight:bold;'>{}</span>".format(u.username, password)
        send_info_mail(u, "Avishkar 2020 Registration", info_msg)

        return Response(context)

class UserLogin(APIView):

    def post(self, request):
        context = {"success": True, "loggedin": False, "temp": False}
        if request.user.is_authenticated:
            context["success"]=False
            context["loggedin"]=True
            return Response(context)
        
        errors = []
        username = request.POST.get("username").strip().lower()
        password = request.POST.get("password")
        
        u = get_user(username)
        ud = None
        if not u:
            errors.append("No Account Found")
            
        elif not u.is_active:
            errors.append("Acount is deactivated. Contact us to activate it.")
            
        else:
            ud = u.userdetails
            if not (ud.temp_pass and password == ud.temp_pass_value):
                u=authenticate(username=u.username, password=password)
            else:
                context["temp"] = True
            
            if not u:
                errors.append("Wrong Password")

        if u and not ud:
            errors.append("Something Went Wrong")

        if errors:
            context["success"]=False
            context["errors"]=errors
            return Response(context)
            
        token = Token.objects.get_or_create(user=u)
        context["token"] = token[0].key
        ud.temp_pass = False
        ud.temp_pass_value = ""
        ud.save()
        
        return Response(context)


class ResetPassword(APIView):

    def post(self, request):
        username = request.POST.get("username").strip().lower()
        context = {"success": True}
        errors = []
        u = User.objects.filter(username=username).first()

        if not u:
            errors.append("User doesnot exist")

        if errors:
            context["errors"] = errors
            return Response(context)

        res = send_password_reset_mail(u)

        if not res:
            context["success"] = False
            context["errors"] = ["Something went wrong"]
            return Response(context)

        context["message"] = "Reset password instructions is sent to {}".format(u.email)
        return Response(context)


class ChangePassword(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        password = request.POST.get("password")
        context = {"success": True}

        if len(password) < 6:
            context["success"] = False
            context["errors"] = ["Password must be of more than 6 characters."]
            return Response(context)

        request.user.set_password(password)
        request.user.save()

        return Response(context)

class UserLogout(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)	

    def post(self, request):
        context = {"success": True}

        request.user.auth_token.delete()

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

        if request.user.userdetails.is_user_confirmed : 
            errors.append("User details already locked.")    

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


class LockUser(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):

        context = {"success": False}
        errors = []

        u = request.user
        ud = request.user.userdetails

        if u.first_name and u.email and ud.college and ud.phone and ud.whatsapp and ud.msteams and ud.resume :
            pass
        else :
            errors.append("User details missing.")

        if errors:
            context["errors"]=errors
            return Response(context)

        ud.confirmed = True 
        ud.save()
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
        resume = request.POST.get("resume").strip()
        registration_number = request.POST.get("regno").strip()

        ud = request.user.userdetails
 
        if not is_valid_number(phone):
            errors.append("Invalid Phone Number")

        if not is_valid_number(whatsapp):
            errors.append("Invalid WhatsApp Number")

        if (not ud.is_fees_paid()) and (college == "" or len(college) == 0 or college == "MNNIT"):
            errors.append("College name 'MNNIT' or empty is not allowed")

        if not registration_number or not msteams or not resume or msteams == "" or resume == "" or len(msteams) == 0 or len(resume) == 0 or registration_number == "" or len(registration_number) == 0:
            errors.append("All details are not filled. Fill NA, if not applicable")


        if errors:
            context["errors"]=errors
            return Response(context)

        
        if not ud.is_fees_paid():
            ud.college = college

        ud.phone = phone
        ud.whatsapp = whatsapp
        ud.msteams_id = msteams
        ud.resume = resume
        ud.registration_number = registration_number

        ud.save()

        context["success"] = True

        return Response(context)



class UpdateFeesStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):

        if not request.user.is_staff:
            context = {"success": False, errors: ["Only staff member can update fees status"]}
            return Response(context)

        context = {"success": False}

        status = request.POST.get("status").strip()
        username = request.POST.get("username").strip()
        
        u = User.objects.filter(username=username).first()
        if not u:
            context = {"success": False, errors: ["{} does not exist".format(username)]}
            return Response(context)
        
        ud = u.userdetails
        
        if status == "paid":
            ud.fees_paid = True
            context["message"] = "Fees paid successfully"
        elif status == "pending":
            ud.fees_paid = False
        
        ud.save()
        context["success"] = True

        return Response(context)

        

class GetUserDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):

        context = {"success": True}
        errors = []

        u = request.user
        ud = request.user.userdetails
        
        context["userName"] = u.username
        context["email"] = u.email
        context["email"] = u.email
        context["firstName"] = u.first_name
        context["lastName"] = u.last_name
        context["confirmed"] = ud.confirmed
        context["feesPaid"] = ud.fees_paid
        context["whatsapp"] = ud.whatsapp
        context["phone"] = ud.phone
        context["college"] = ud.college
        context["msteamsID"] = ud.msteams_id
        context["resume"] = ud.resume
        context["notifications"] = ud.notifications
        context["isStaff"] = u.is_staff
        context["teams"] = {}



        for x in EventTeam.objects.all():
            if u in x.team_members.all() or u in x.pending_members.all():
                context["teams"][x.team_id] = {
                    "teamID":x.team_id,
                    "teamAdmin":x.team_admin.username,
                    "teamName":x.team_name,
                    "teamMembers":[],
                    "pendingMembers":[],
                    "registeredEvents":{},
                }
                for y in x.pending_members.all():
                    context["teams"][x.team_id]["pendingMembers"].append(y.username)
                for y in x.team_members.all():
                    context["teams"][x.team_id]["teamMembers"].append(y.username)

                for y in Event.objects.all():
                    if x in y.registered_teams.all():
                        context["teams"][x.team_id]["registeredEvents"][y.event_id] = {
                            "eventName":y.event_name,
                            "eventID":y.event_id,
                            "eventParent":y.event_parent,
                        }


        return Response(context)


class GetUserDetailsByUsername(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):

        context = {"success": True}
        errors = []

        if not request.user.is_staff:
            context = {"success": False, "errors" : ["Only staff members can access user details by username"]}
            return Response(context)

        username = request.POST.get("username").strip()

        u = User.objects.filter(username=username).first()

        if not u:
            context = {"success": False, "errors" : ["{} does not exist".format(username)]}
            return Response(context)

        ud = u.userdetails
        
        context["userName"] = u.username
        context["email"] = u.email
        context["email"] = u.email
        context["firstName"] = u.first_name
        context["lastName"] = u.last_name
        context["confirmed"] = ud.confirmed
        context["feesPaid"] = ud.fees_paid
        context["whatsapp"] = ud.whatsapp
        context["phone"] = ud.phone
        context["college"] = ud.college
        context["msteamsID"] = ud.msteams_id
        context["resume"] = ud.resume
        context["notifications"] = ud.notifications
        context["teams"] = {}



        for x in EventTeam.objects.all():
            if u in x.team_members.all():
                context["teams"][x.team_id] = {
                    "teamID":x.team_id,
                    "teamAdmin":x.team_admin.username,
                    "teamName":x.team_name,
                    "teamMembers":[],
                    "pendingMembers":[],
                    "registeredEvents":{},
                }
                for y in x.pending_members.all():
                    context["teams"][x.team_id]["pendingMembers"].append(y.username)
                for y in x.team_members.all():
                    context["teams"][x.team_id]["teamMembers"].append(y.username)

                for y in Event.objects.all():
                    if x in y.registered_teams.all():
                        context["teams"][x.team_id]["registeredEvents"][y.event_id] = {
                            "eventName":y.event_name,
                            "eventID":y.event_id,
                        }


        return Response(context)


