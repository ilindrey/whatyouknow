from django.template.loader import render_to_string

from django.contrib.contenttypes.models import ContentType

from .models import Comment


def render_parent_comments(obj):
    comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj),
                                      object_id=obj.pk,
                                      parent=None)
    context = {'comments': comments}
    return render_to_string('comment_base.html', context)
