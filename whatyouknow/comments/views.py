from django.shortcuts import render

from django.template import loader
from django.http import JsonResponse


from .models import Comment


def comment_children(request):

    parent_id = request.GET.get('parent_id')

    if parent_id:
        comments = Comment.objects.filter(parent_id=parent_id).order_by('posted')
        # build a html posts list with the paginated posts
        comments = loader.render_to_string('comment_children_tree.html', {'comments': comments})
        # package output data and return it as a JSON object
        output_data = {
            'comment_children': comments
            }
        return JsonResponse(output_data, status=200)
    return JsonResponse({"error": ""}, status=400)
