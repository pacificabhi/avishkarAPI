from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .validations import *
from .models import UserDetails
from events.models import EventTeam,Event

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
        if is_mnnit == "true":
            ud.college = "MNNIT"
            ud.fees_paid = True
            ud.save()

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
        resume = request.POST.get("resume").strip()

        if not is_valid_number(phone):
            errors.append("Invalid Phone Number")

        if not is_valid_number(whatsapp):
            errors.append("Invalid WhatsApp Number")

        if college == "MNNIT":
            errors.append("College name MNNIT is not allowed")

        if errors:
            context["errors"]=errors
            return Response(context)

        ud = request.user.userdetails
        if not ud.is_fees_paid():
            ud.college = college
        ud.phone = phone
        ud.whatsapp = whatsapp
        ud.msteams_id = msteams
        ud.resume = resume

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


