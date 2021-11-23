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


@register.inclusion_tag('moderation/link_to_moderation.html', takes_context=True)
def link_to_moderation(context, obj=None, name='Moderation', as_button=True, extra_button_class='primary basic',
                       show_icon=True, icon='primary gavel icon'):
    if obj is None:
        obj = context.get('object')
    user = context.get('request').user
    return {
        'object': obj,
        'user': user,
        'name': name,
        'as_button': as_button,
        'extra_button_class': extra_button_class,
        'show_icon': show_icon,
        'icon': icon
    }
