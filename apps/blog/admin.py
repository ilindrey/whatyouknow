from django.contrib.admin import register

from django_summernote.admin import SummernoteModelAdmin

from ..moderation.admin import ModeratedObjectAdmin
from .models import Post


@register(Post)
class PostAdmin(ModeratedObjectAdmin, SummernoteModelAdmin):
    list_display = ('__str__', 'user', 'category')
    search_fields = ('title', 'user__username')
    list_filter = ('category', )
    ordering = ('-date_updated', )
    readonly_fields = ('user',)
    summernote_fields = ('feed_article_preview', 'text')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)
