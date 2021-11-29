from django.template import Library
from django.db.models import Model
from django.contrib.contenttypes.models import ContentType

from apps.comments.models import Comment


register = Library()

ERROR_MESSAGE = 'Invalid argument, obj is not a model'


@register.inclusion_tag('comments/base.html', takes_context=True)
def render_comments(context, obj):
    assert isinstance(obj, Model), ERROR_MESSAGE
    obj_data = {
        'app_label': obj._meta.app_label,
        'model_name': obj._meta.model_name,
        'model_pk': obj.pk,
        'is_draft': obj.is_draft,
        'is_pending': obj.is_pending,
        'is_pending': obj.is_moderated,
        'is_pending': obj.is_approved,
        'is_pending': obj.is_rejected,
        'published': obj.published
    }
    return {
        'object': obj_data,
        'comments_count': comments_count(obj),
        'user': context.get('request').user
    }


@register.simple_tag
def comments_count(obj):
    assert isinstance(obj, Model), ERROR_MESSAGE
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()
