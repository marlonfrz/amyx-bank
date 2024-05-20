from django.contrib import admin

from .models import Profile


# Register your models here.
@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ['id', 'user', 'avatar', 'status', 'date_of_birth']
