
from django.template import Library
from django.template.loader import render_to_string

from apps.core.utils import author_or_has_permssions


register = Library()


@register.simple_tag(takes_context=True)
def post_edit_button(context, obj=None):
    if obj is None:
        obj = context.get('object')
    request = context.get('request')
    user = request.user
    if author_or_has_permssions(user, obj):
        return render_to_string('blog/post/edit/buttons/edit_post.html',
                                context={'object': obj, 'user': user},
                                request=request)
    else:
        return ''
