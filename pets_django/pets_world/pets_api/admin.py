from django.contrib import admin

from .models import UserData, CustomUser

# Register your models here.

admin.site.register(UserData)
admin.site.register(CustomUser)
