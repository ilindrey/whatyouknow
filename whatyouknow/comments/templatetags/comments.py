from django import template

from whatyouknow.comments.utils import render_parent_comments

register = template.Library()


@register.simple_tag
def render_comments(obj):
    return render_parent_comments(obj)