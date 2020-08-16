from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import *



class CreateTeam(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


    def post(self, request):
        u = request.user

        if u.is_staff:
            context = {"success": False, "errors": ["You are an event staff member, You can not create teams"]}
            return Response(context)

        team_name = request.POST.get("teamname").strip()
        team = EventTeam.objects.create(team_name=team_name, team_admin=u)
 
        team_id = "TEAM" + str(team.pk)
        team.team_id = team_id

        team.add_team_member(u)
        team.save()

        context = {"success": True, "team_id": team_id}

        return Response(context)


class AddTeamMember(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):

        team_id = request.POST.get("teamid").strip()
        team = EventTeam.objects.filter(team_id=team_id).first()

        if not team:
            context = {"success": False, "errors" : ["Team with team id {} is not found".format(team_id)]}
            return Response(context)

        if request.user != team.team_admin:
            context = {"success": False, "errors" : ["You are not admin of team {}".format(team_id)]}
            return Response(context)

        if len(team.participants.all()) > 0:
            context = {"success": False, "errors" : ["Team {} is already registerd in some event so it can not be edit".format(team_id)]}
            return Response(context)

        member_username = request.POST.get("memberusername").strip()
        member = User.objects.filter(username=member_username).first()

        if not member:
            context = {"success": False, "errors" : ["User with username {} is not found".format(member_username)]}
            return Response(context)

        if member.is_staff:
            context = {"success": False, "errors" : ["User with username {} is staff member".format(member_username)]}
            return Response(context)

        if not member.userdetails.is_fees_paid():
            context = {"success": False, "errors" : ["User with username {} is not eligible because of not paying registration fees".format(member_username)]}
            return Response(context)

        if member in team.team_members.all():
            context = {"success": False, "errors" : ["User with username {} is already a team member".format(member_username)]}
            return Response(context)

        if member in team.pending_members.all():
            context = {"success": False, "errors" : ["Join Team request has been already sent to {}".format(member_username)]}
            return Response(context)

        is_mnnit = False
        if team.team_admin.userdetails.college == "MNNIT":
            is_mnnit = True

        if is_mnnit and not member.userdetails.college =="MNNIT":
            context = {"success": False, "errors" : ["You can add only users from MNNIT"]}
            return Response(context)

        team.pending_members.add(member)

        context = {"success": True, "message" : "Join Team request has been sent to {}".format(member_username)}
        return Response(context)


class RemoveTeamMember(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


    def post(self, request):
        team_id = request.POST.get("teamid").strip()
        team = EventTeam.objects.filter(team_id=team_id).first()

        if not team:
            context = {"success": False, "errors" : ["Team with team id {} is not found".format(team_id)]}
            return Response(context)

        if len(team.participants.all()) > 0:
            context = {"success": False, "errors" : ["Team {} is already registerd in some event so it can not be edit".format(team_id)]}
            return Response(context)
        
        member_username = request.POST.get("memberusername").strip()
        member = User.objects.filter(username=member_username).first()

        if not member:
            context = {"success": False, "errors" : ["User with username {} does not exist".format(member_username)]}
            return Response(context)
        
        if request.user != team.team_admin and request.user != member:
            context = {"success": False, "errors" : ["Only admin can remove members from team or one can remove themselves"]}
            return Response(context)


        if member in team.team_members.all():
            team.team_members.remove(member)
            context = {"success": True, "errors" : ["{} is successfully removed from team {}".format(member_username, team_id)]}
            return Response(context)

        if member in team.pending_members.all():
            team.pending_members.remove(member)
            context = {"success": True, "errors" : ["{} is successfully removed from team {}".format(member_username, team_id)]}
            return Response(context)


        context = {"success": False, "errors" : ["{} is not a member of team {}".format(member_username, team_id)]}
        return Response(context)


class JoinRequestDecision(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


    def post(self, request):
        team_id = request.POST.get("teamid").strip()
        decision = request.POST.get("decision").strip()
        team = EventTeam.objects.filter(team_id=team_id).first()

        if not team:
            context = {"success": False, "errors" : ["Team with team id {} is not found".format(team_id)]}
            return Response(context)

        member = request.user
        member_username = member.username

        if not member:
            context = {"success": False, "errors" : ["User with username {} does not exist".format(member_username)]}
            return Response(context)


        if member in team.team_members.all():
            context = {"success": False, "errors" : ["{} is already a member of team {}".format(member_username, team_id)]}
            return Response(context)

        if member in team.pending_members.all():
            team.pending_members.remove(member)
            if decision == "accept":
                team.team_members.add(member)
                context = {"success": True, "errors" : ["{} is successfully added to team {}".format(member_username, team_id)]}
            else:
                context = {"success": True, "errors" : ["{} has declined to join team {}".format(member_username, team_id)]}

            return Response(context)

        context = {"success": False, "errors" : ["No Join Request"]}
        return Response(context)
        


class RegisterToEvent(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


    def post(self, request):
        team_id = request.POST.get("teamid").strip()
        event_id = request.POST.get("eventid").strip()

        event = Event.objects.filter(event_id=event_id).first()

        if not event:
            context = {"success": False, "errors" : ["Event with event id {} is not found".format(event_id)]}
            return Response(context)

        if not event.can_register():
            context = {"success": False, "errors" : ["Registration for this contest is closed"]}
            return Response(context)

        team = EventTeam.objects.filter(team_id=team_id).first()
        if not team:
            context = {"success": False, "errors" : ["Team with team id {} is not found".format(team_id)]}
            return Response(context)

        if request.user != team.team_admin:
            context = {"success": False, "errors" : ["Only admin can register team to contest"]}
            return Response(context)

        if not event.is_open() and team.team_admin.userdetails.college != "MNNIT":
            context = {"success": False, "errors" : ["This event is exclusively for MNNIT students"]}
            return Response(context)

        if not team.is_ready():
            context = {"success": False, "errors" : ["Team is not ready to register, Team has some pending members request(s)"]}
            return Response(context)


        if team.get_teamsize() > event.get_teamsize():
            context = {"success": False, "errors" : ["Team has more number of members than event maximum team size"]}
            return Response(context)


        registered_teams = event.registered_teams.all()

        if team in registered_teams:
            context = {"success": False, "errors" : ["Team is already registered to this event"]}
            return Response(context)

        team_members = team.team_members.all()

        already_members = []
        for in_team in registered_teams:
            for member in team_members:
                if member in in_team.team_members.all():
                    already_members.append((member, in_team))

        if already_members:
            errors = ["Some members of team is already in other team in the same event."]
            for member, in_team in already_members:
                errors.append("{} is member of {}".format(member.username, in_team.team_id))
            
            context = {"success": False, "errors" : errors}
            return Response(context)


        event.registered_teams.add(team)
        event.save()

        context = {"success": True, "errors" : ["Team is successfully registered to this event"]}
        return Response(context)
        

# Returns a list to team members with team details

def getTeamDetails(team):
    team_details = {
        "team_id": team.team_id,
        "team_admin": team.team_admin.username,
        "team_size": team.get_teamsize(),
    }
    team_m = []
    for u in team.team_members.all():
        context = {}
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

        team_m.append(context)

    team_details["team_members"] = team_m

    return team_details

class GetRegisteredUsersListOfEvent(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


    def post(self, request):


        if not request.user.is_staff:
            context = {"success": False, "errors" : ["Only staff members can access details of registered users in an event"]}
            return Response(context)


        event_id = request.POST.get("eventid").strip()
        event = Event.objects.filter(event_id=event_id).first()

        if not event:
            context = {"success": False, "errors" : ["{} does not exist".format(event_id)]}
            return Response(context)

        
        registered_teams = event.registered_teams.all()

        context = {"success": True, "teams": []}
        teams = []
        for team in registered_teams:
            teams.append(getTeamDetails(team))

        context["teams"] = teams

        return Response(context)


class GetTeamDetails(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

    def post(self, request):
        
        if not request.user.is_staff:
            context = {"success": False, "errors" : ["Only staff members can access details of a team"]}
            return Response(context)

        team_id = request.POST.get("teamid").strip()
        team = EventTeam.objects.filter(team_id=team_id).first()

        if not team:
            context = {"success": False, "errors" : ["Team does not exist - {}".format(team_id)]}
            return Response(context)

        team_details = getTeamDetails(team)
        context = {"success": True, "team_details": team_details}

        return Response(context)