from django.contrib import admin
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars

from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter

from .models import Comment
from ..moderation.admin import ModeratedObjectAdmin


# class CommentProxy(Comment):
#     class Meta:
#         proxy = True
#         app_label = 'blog'
#         verbose_name = 'Comment'


@admin.register(Comment)
class CommentAdmin(ModeratedObjectAdmin, MPTTModelAdmin, admin.ModelAdmin):

    list_display = ('text_representation', 'user', 'content_object_representation')
    search_fields = ('text', 'user', 'content_object_representation')
    readonly_fields = ('user',)
    list_display_links = ('text_representation',)
    readonly_fields = ('user', 'content_object_representation_clickable')
    mptt_indent_field = 'text_representation'
    list_filter = (('parent', TreeRelatedFieldListFilter),)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description='Object')
    def content_object_representation(self, instance):
        obj__str__ = truncatechars(instance.content_object.__str__(), 50)
        return '%s: id%s | %s ' % (instance.content_type.name.capitalize(), instance.object_id, obj__str__)
    # content_object_representation.short_description = 'Object'

    @admin.display(description='Object')
    def content_object_representation_clickable(self, instance):
        return format_html("<a href='{}'>{}</a>",
                           instance.content_object.get_admin_url(),
                           self.content_object_representation(instance))
    # content_object_representation_clickable.short_description = 'Object'

