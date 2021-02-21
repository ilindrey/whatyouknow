from django.shortcuts import render

from django.template.loader import render_to_string
from django.http import JsonResponse

from django.contrib.contenttypes.models import ContentType


from .models import Comment
from .utils import render_parent_comments


def comment_parents(request, obj):
    return render(request, render_parent_comments(obj))


def comment_children(request):

    parent_id = request.GET.get('parent_id')

    if request.is_ajax() and parent_id:
        comments = Comment.objects.filter(parent_id=parent_id)
        # build a html posts list with the paginated posts
        template = render_to_string('comment_children_tree.html', {'comments': comments})
        # package output data and return it as a JSON object
        output_data = {
            'comment_children': template
            }
        return JsonResponse(output_data, status=200)
    return JsonResponse({"error": ""}, status=400)
