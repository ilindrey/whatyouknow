from django.http import JsonResponse
from django.views.generic import RedirectView, FormView, ListView, TemplateView

from taggit.models import Tag

from apps.blog.models import Post, CategoryTypes

from .forms import SearchForm


class IndexView(RedirectView):
    pattern_name = 'post_list_default'


class SearchView(FormView):
    form_class = SearchForm
    template_name = 'core/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'cur_page': self.kwargs.get('page', 1)
            })
        return context


class SearchContainerView(SearchView):
    template_name = 'core/search/container.html'


class SearchSuitableResultsListView(TemplateView):
    max_results = 10

    def get_result_list(self, context):
        query = self.request.GET.get('query')

        categories = CategoryTypes.get('short_name_lower', 'full_name')
        posts = Post.objects.filter(title__startswith=query).order_by('title') \
                    .values_list('title', flat=True)[:self.max_results]
        tags = Tag.objects.filter(name__startswith=query).order_by('name') \
                    .values_list('name', flat=True)[:self.max_results]

        j = []
        for value in categories:
            j.append({
                'icon': 'stream',
                'value': value['short_name_lower'],
                'title': value['full_name'],
                'type': 'category'
                })

        for value in posts:
            j.append({
                'icon': '',
                'value': value,
                'title': value,
                'type': 'text'
                })

        for value in tags:
            j.append({
                'icon': 'tag',
                'value': value,
                'title': value,
                'type': 'tag'
                })

        j_rd = [dict(t) for t in {tuple(d.items()) for d in j}]  # remove duplicates
        s = sorted(j_rd, key=lambda x: x['title'].lower())
        l = list(filter(lambda item: item['title'].lower().startswith(query.lower()), s))
        return l[:self.max_results]

    def render_to_response(self, context, **response_kwargs):
        result_list = self.get_result_list(context)
        json = {"results": result_list}
        return JsonResponse(data=json, status=200)


class SearchSelectionsView(TemplateView):
    template_name = 'core/search/selections.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        text = self.request.GET.get('text')
        tag_list = self.request.GET.getlist('tag')
        category_list = self.request.GET.getlist('category')

        context.update({
            'text': text,
            'category_list': CategoryTypes.get_values(*category_list, key='short_name_lower'),
            'tag_list': tag_list,
            })
        return context

