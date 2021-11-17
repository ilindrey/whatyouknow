from django.contrib import admin

from .models import Comment
from ..moderation.admin import ModeratedObjectAdmin


@admin.register(Comment)
class CommentAdmin(ModeratedObjectAdmin, admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


# admin.site.register(Comment, CommentAdmin)
