from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Profile


class ProfileAdmin(UserAdmin):

    fieldsets = (
        (_("Personal info"), {"fields": ("avatar", "username", "name", "email", "password", "description")}),
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
    list_display = ("username", "email", "name", "is_staff")
    search_fields = ("username", "name", "email")


admin.site.register(Profile, ProfileAdmin)
