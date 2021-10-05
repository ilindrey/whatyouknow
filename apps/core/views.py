from django.http import JsonResponse
from django.views.generic import RedirectView, FormView, ListView, TemplateView

from taggit.models import Tag

from apps.blog.models import Post, CategoryTypes

from .forms import SearchForm


class IndexView(RedirectView):
    pattern_name = 'post_list'


class SearchView(FormView):
    form_class = SearchForm
    template_name = 'core/search.html'


class SearchContainerView(SearchView):
    template_name = 'core/search/container.html'


class SearchDropdownResultsView(TemplateView):
    filtering_by = 10

    def get_result_list(self, context):
        query = self.request.GET.get('query')

        categories = CategoryTypes.list('full_name')
        posts = Post.objects.filter(title__startswith=query).order_by('title') \
                    .values_list('title', flat=True)[:self.filtering_by]
        tags = Tag.objects.filter(name__startswith=query).order_by('name') \
                    .values_list('name', flat=True)[:self.filtering_by]

        result_list = []
        for value in categories:
            result_list.append({
                'icon': 'stream',
                'title': value,
                'type': 'category'
                })

        for value in posts:
            result_list.append({
                'icon': '',
                'title': value,
                'type': 'query'
                })

        for value in tags:
            result_list.append({
                'icon': 'tag',
                'title': value,
                'type': 'tag'
                })

        s = sorted(result_list, key=lambda x: x['title'].lower())
        l = list(filter(lambda item: item['title'].lower().startswith(query.lower()), s))
        return l[:self.filtering_by]

    def render_to_response(self, context, **response_kwargs):
        result_list = self.get_result_list(context)
        json = {"results": result_list}
        return JsonResponse(data=json, status=200)
