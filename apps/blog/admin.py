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

    def get_fields(self, request, obj=None, **kwargs):
        fields = list(super().get_fields(request, obj, **kwargs))
        fields.remove('slug')
        fields.insert(2, 'slug')
        return fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)
