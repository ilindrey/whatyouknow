from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Post, CategoryTypes


class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    paginate_by = 10
    ordering = '-publish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryTypes.choices()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
