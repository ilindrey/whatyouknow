from django.template import Library


register = Library()


@register.simple_tag
def get_avatar(user, size):
    return user.get_avatar(size)
