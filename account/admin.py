from django.contrib import admin

from .models import DeletedUser, Profile


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['id', 'user', 'avatar', 'status', 'date_of_birth']




admin.register(DeletedUser)
