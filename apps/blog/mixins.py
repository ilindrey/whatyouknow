from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Post
from .forms import EditPostForm


class PostCreateEditFormMixin(LoginRequiredMixin):
    model = Post
    form_class = EditPostForm

    def get_success_url(self):
        preview = eval(self.request.POST.get('preview').capitalize())
        kwargs = {'pk': self.object.pk}
        if preview:
            return reverse('post_preview_container', kwargs=kwargs)
        else:
            return reverse('post_edit_container', kwargs=kwargs)
