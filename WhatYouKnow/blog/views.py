from django.shortcuts import render
from django.core.serializers import serialize
from django.http import JsonResponse

from .models import Category


def index(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
        }
    return render(request, 'base.html', context)


# def search_list(request):
#     if request.is_ajax() and request.method == 'GET':
#         search = request.GET.get('search')
#         category = Category.objects.filter(name__icontains=search).order_by('id')
#         instance = serialize('json', [category,])
#         return JsonResponse({'instance': instance}, status=200)
#     return JsonResponse({}, status=400)



