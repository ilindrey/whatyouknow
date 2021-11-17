from django.contrib import admin

from apps.moderation.admin import ModeratedObjectAdmin

from .models import Post


@admin.register(Post)
class PostAdmin(ModeratedObjectAdmin, admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


# admin.site.register(Post, PostAdmin)
