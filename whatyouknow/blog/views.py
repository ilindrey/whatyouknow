from django.shortcuts import render
from django.core.serializers import serialize
from django.http import JsonResponse
from django.db.models import F

from .models import Post, CATEGORY_CHOICES


def index(request):
    # categories = Category.objects.all()
    posts = Post.objects.all().order_by('-date')[:10]
    tags = Post.objects.values(post_id=F('id')).values('post_id', name=F('tags__name'))
    context = {
        # 'categories': categories,
        'posts': posts,
        'tags': tags
        }
    return render(request, 'base.html', context)


# def search_list(request):
#     if request.is_ajax() and request.method == 'GET':
#         search = request.GET.get('search')
#         category = Category.objects.filter(name__icontains=search).order_by('id')
#         instance = serialize('json', [category,])
#         return JsonResponse({'instance': instance}, status=200)
#     return JsonResponse({}, status=400)



