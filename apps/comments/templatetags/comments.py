from django import template
from django.db.models import Model
from django.http import Http404
from django.contrib.contenttypes.models import ContentType

from apps.comments.models import Comment

register = template.Library()


@register.inclusion_tag('comments/base.html', takes_context=True)
def render_comments(context, obj):
    if not is_model(obj):
        return
    obj_data = {
        'app_label': obj._meta.app_label,
        'model_name': obj._meta.model_name,
        'model_pk': obj.pk
        }
    obj_comment_count = comments_count(obj)
    return {
        'obj': obj_data,
        'comments_count': obj_comment_count,
        'user': context['request'].user
        }


@register.simple_tag
def comments_count(obj):
    if not is_model(obj):
        return
    return Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj),
                                  object_id=obj.pk).count()


def is_model(obj):
    if not isinstance(obj, Model):
        raise Http404(str(obj) + ' is not a model object.')
    return True
