from django.contrib import admin
from .models import UserDetails

# Register your models here.


class UserDetailsAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)


admin.site.register(UserDetails, UserDetailsAdmin)