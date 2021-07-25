from django.core.files.uploadedfile import UploadedFile, InMemoryUploadedFile, TemporaryUploadedFile
from django.shortcuts import reverse
from django.views.generic import DetailView, ListView, TemplateView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import caches, cache
from django.core.files.images import ImageFile
from io import BytesIO

from .models import Post, CategoryTypes
from .forms import PostWriteForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    paginate_by = 15
    ordering = '-publish'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['categories'] = CategoryTypes.get_list()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(TemplateView):
    template_name = 'blog/post_create.html'


class PostWriteView(LoginRequiredMixin, FormView):
    form_class = PostWriteForm
    template_name = 'blog/post_create/write.html'

    def get_initial(self):
        fields = list(self.form_class.Meta.fields)
        fields.remove('feed_cover')
        for field in fields:
            self.initial[field] = self.request.session.get(field)
        return super().get_initial()

    def form_valid(self, form):

        fields = form.fields.copy()
        del fields['feed_cover']
        for field in fields:
            if field in 'tags':
                tags = []
                for tag in form.cleaned_data[field]:
                    tags.append({'name': tag})
                self.request.session[field] = tags
            else:
                self.request.session[field] = form.cleaned_data[field]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_preview')


class PostPreviewView(CreateView):
    form_class = PostWriteForm
    template_name = 'blog/post_create/preview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class PostDoneView(TemplateView):
    template_name = 'blog/post_create/done.html'
