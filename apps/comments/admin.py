from django.contrib import admin
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars

from django_summernote.admin import SummernoteModelAdmin
from mptt.admin import MPTTModelAdmin

from ..moderation.admin import ModeratedObjectAdmin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(ModeratedObjectAdmin, MPTTModelAdmin, SummernoteModelAdmin):

    list_display = ('text_representation', 'user', 'content_object_representation')
    list_display_links = ('text_representation',)
    search_fields = ('text', 'user__username')
    readonly_fields = ('user', 'content_object_representation_clickable_link')
    mptt_indent_field = 'text_representation'
    autocomplete_lookup_fields = {
        'generic': ['content_type', 'object_id'],
    }
    summernote_fields = ('text', )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='Object')
    def content_object_representation(self, instance):
        obj__str__ = truncatechars(instance.content_object.__str__(), 50)
        return '%s: id%s | %s ' % (instance.content_type.name.capitalize(), instance.object_id, obj__str__)

    @admin.display(description='Object')
    def content_object_representation_clickable_link(self, instance):
        return format_html("<a href='{}'>{}</a>",
                           instance.content_object.get_admin_url(),
                           self.content_object_representation(instance))
