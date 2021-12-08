from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Post
from .forms import EditPostForm


class ArtualObjectKwargsMixin:

    @property
    def get_kwargs(self):
        if self.object is not None and self.object.pk is not None:
            return {'pk': self.object.pk, 'slug': self.object.slug}
        else:
            {}


class PostCreateEditFormMixin(LoginRequiredMixin, ArtualObjectKwargsMixin):
    model = Post
    form_class = EditPostForm

    def get_success_url(self):
        if self.request.POST.get('next_action') == 'preview':
            return reverse('post_preview_container', kwargs=self.get_kwargs)
        else:
            return reverse('post_edit_container', kwargs=self.get_kwargs)
