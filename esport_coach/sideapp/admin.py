from django.contrib import admin
from .models import *
from .forms import *

class adminCoach(admin.ModelAdmin):
    list_display = ('server', 'champion', 'rating', 'pricerate', 'role', 'avatar', 'overview')

class adminUser(admin.ModelAdmin):
    list_display = ('userid', 'password', 'pname', 'email', 'rank', 'skypeid', 'twitchid')

admin.site.register(Coach, adminCoach)
admin.site.register(User, adminUser)