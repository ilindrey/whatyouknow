from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# from rest_framework.authtoken.models import Token, TokenProxy as DefaultTokenProxy
# from rest_framework.authtoken.admin import TokenAdmin

from .models import Profile


# class GroupProxy(Group):
#     class Meta:
#         proxy = True
#         app_label = 'profiles'
#         verbose_name = 'Group'
#
#
# class TokenProxy(Token):
#     class Meta:
#         proxy = True
#         app_label = 'profiles'
#         verbose_name = 'Token'


class ProfileAdmin(UserAdmin):

    fieldsets = (
        (_("Personal info"), {"fields": ("avatar", "username", "email", "name", "password", "description")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("User settings"), {"fields": ("settings", )}),
    )
    list_display = ("username", "name",  "email", 'is_active', "is_staff", 'is_superuser')
    search_fields = ("username", "name", "email")


# admin.site.unregister(Group)
# admin.site.unregister(DefaultTokenProxy)

admin.site.register(Profile, ProfileAdmin)
# admin.site.register(GroupProxy, GroupAdmin)
# admin.site.register(TokenProxy, TokenAdmin)
