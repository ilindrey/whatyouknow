from django.contrib import admin

from .models import Comment
from ..moderation.admin import ModeratedObjectAdmin


@admin.register(Comment)
class PostAdmin(ModeratedObjectAdmin, admin.ModelAdmin):
    pass

# Register your models here.
# admin.site.register(Comment)
