from django import template

register = template.Library()


@register.simple_tag
def get_avatar(user, size):
    return user.get_avatar(size)
