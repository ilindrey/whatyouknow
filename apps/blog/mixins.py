from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Post
from .forms import EditPostForm


class PostCreateEditFormMixin(LoginRequiredMixin):
    model = Post
    form_class = EditPostForm

    # def get_context_data(self):

    def get_success_url(self):
        preview = bool(self.request.POST.get('preview'))
        kwargs = {'pk': self.object.pk}
        if preview:
            return reverse('post_preview_load_data', kwargs=kwargs)
        else:
            return reverse('post_edit_load_data', kwargs=kwargs)
