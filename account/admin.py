from django.contrib import admin

from .models import Profile, DeletedUser


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['id', 'avatar', 'status', 'date_of_birth']




admin.register(DeletedUser)
