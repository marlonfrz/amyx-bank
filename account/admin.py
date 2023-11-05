from django.contrib import admin

from .models import Profile, DeletedUser

admin.register(Profile)
admin.register(DeletedUser)