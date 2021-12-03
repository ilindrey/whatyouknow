from django.contrib.admin import register

from django_summernote.admin import SummernoteModelAdmin

from ..moderation.admin import ModeratedObjectAdmin
from .models import Post
from .forms import EditPostAdminForm


@register(Post)
class PostAdmin(ModeratedObjectAdmin, SummernoteModelAdmin):
    form = EditPostAdminForm
    list_display = ('__str__', 'user', 'category')
    list_filter = ('category', )
    search_fields = ('title', 'user__username')
    ordering = ('-date_updated', )
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('user',)
    summernote_fields = ('feed_article_preview', 'text')
    # fields = ('category', 'title', 'slug', 'feed_cover', 'feed_article_preview',
    #           'text', 'tags', 'user', 'date_created', 'date_updated', 'date_published')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)
