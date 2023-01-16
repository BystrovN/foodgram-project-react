from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Follow


class CustomUserAdmin(UserAdmin):
    list_filter = ('id', 'email', 'username')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow, FollowAdmin)
