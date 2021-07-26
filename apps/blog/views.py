from django.shortcuts import reverse
from django.views.generic import DetailView, ListView, TemplateView, FormView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, CategoryTypes
from .forms import EditPostForm


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


class PostCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/post/create.html'


class PostWriteView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = EditPostForm
    template_name = 'blog/post/create/write.html'


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = EditPostForm
    template_name = 'blog/post/create/forms/edit_post.html'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk', self.object.pk})


class PostPreviewView(DetailView):
    model = Post
    template_name = 'blog/post/create/preview.html'


class PostDoneView(TemplateView):
    template_name = 'blog/post/create/done.html'
