from django.shortcuts import reverse
from django.views.generic import DetailView, ListView, TemplateView, RedirectView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, CategoryTypes
from .mixins import PostCreateEditFormMixin


class PostListView(ListView):
    model = Post
    template_name = 'blog/post/list.html'
    paginate_by = 15
    ordering = '-published'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['categories'] = CategoryTypes.get_list()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'


class PostCreateView(PostCreateEditFormMixin, CreateView):
    template_name = 'blog/post/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['post_write_url'] = reverse('post_create_load_data')
        context['cur_url'] = reverse('post_create')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostEditView(PostCreateEditFormMixin, UpdateView):
    template_name = 'blog/post/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['post_write_url'] = reverse('post_edit_load_data', kwargs=self.kwargs)
        context['cur_url'] = reverse('post_edit', kwargs=self.kwargs)
        return context


class PostPreviewView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/post/preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['cur_url'] = reverse('post_preview', kwargs=self.kwargs)
        return context


class PostDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/post/done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['cur_url'] = reverse('post_done', kwargs=self.kwargs)
        return context


class PostCreateContainerView(PostCreateView):
    template_name = 'blog/post/edit/container.html'


class PostEditContainerView(PostEditView):
    template_name = 'blog/post/edit/container.html'


class PostPreviewContainerView(PostPreviewView):
    template_name = 'blog/post/preview/container.html'


class PostDoneContainerView(PostDoneView):
    template_name = 'blog/post/done/container.html'
