from django.contrib import admin
from .models import *
# Register your models here.


class EventTeamAdmin(admin.ModelAdmin):
    search_fields = ('team_id',)

admin.site.register(EventTeam, EventTeamAdmin)
admin.site.register(Event)