from django import template

register = template.Library()


@register.inclusion_tag('comments/base.html')
def render_comments(obj):
    obj = {
        'app_label': obj._meta.app_label,
        'model_name': obj._meta.model_name,
        'model_pk': obj.pk
        }
    return {
        'obj': obj
        }
