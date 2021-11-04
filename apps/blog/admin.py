from django.contrib import admin

from moderation.admin import ModerationAdmin

from .models import Post


class PostAdmin(ModerationAdmin):
    pass


admin.site.register(Post, PostAdmin)
