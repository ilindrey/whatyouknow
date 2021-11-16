from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import pre_save

from .models import Comment
from .mixins import ContentTypeObjectCommentMixin, CreateUpdateCommentMixin
from ..moderation.handlers import save_as_approved


class CommentListView(ContentTypeObjectCommentMixin, ListView):
    model = Comment
    template_name = 'comments/list.html'

    def get_queryset(self):
        return super().get_queryset()\
            .filter(content_type=self.content_type,
                    object_id=self.ct_object.pk).extra_fields_status_moderation()


class CreateCommentView(CreateUpdateCommentMixin, LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.content_type = self.content_type
        form.instance.object_id = self.ct_object.pk
        if 'reply' in self.request.POST.get('action_type'):
            form.instance.parent_id = self.request.POST.get('target_id')
        pre_save.connect(save_as_approved)
        return super().form_valid(form)


class EditCommentView(CreateUpdateCommentMixin, LoginRequiredMixin, UpdateView):
    pass
