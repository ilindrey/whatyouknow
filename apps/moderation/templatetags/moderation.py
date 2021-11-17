from django import template

register = template.Library()


@register.inclusion_tag('moderation/status_label.html', takes_context=True)
def status_moderation(context, obj=None, representation_object_name=None):
    if obj is None:
        obj = context.get('object')
    if representation_object_name is None:
        representation_object_name = obj._meta.model_name
    return {
        'object': obj,
        'representation_object_name': representation_object_name,
        }
