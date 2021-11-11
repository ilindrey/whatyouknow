from django.contrib import admin

from apps.moderation.admin import ModeratedObjectAdmin

from .models import Post


@admin.register(Post)
class PostAdmin(ModeratedObjectAdmin, admin.ModelAdmin):
    pass


# admin.site.register(Post, PostAdmin)
