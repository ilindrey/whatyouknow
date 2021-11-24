from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..moderation.views import SetEditedByUserMixin
from .models import Comment
from .mixins import ContentTypeObjectCommentMixin, CreateUpdateCommentMixin


class CommentListView(ContentTypeObjectCommentMixin, ListView):
    model = Comment
    template_name = 'comments/list.html'

    def get_queryset(self):
        return super().get_queryset()\
            .filter(content_type=self.content_type,
                    object_id=self.ct_object.pk)


class CreateCommentView(CreateUpdateCommentMixin, LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.content_type = self.content_type
        form.instance.object_id = self.ct_object.pk
        if 'reply' in self.request.POST.get('action_type'):
            form.instance.parent_id = self.request.POST.get('target_id')
        self.object = form.save()
        if self.object:
            self.object.save_as_published()
        return HttpResponseRedirect(self.get_success_url())


class EditCommentView(CreateUpdateCommentMixin, SetEditedByUserMixin, LoginRequiredMixin, UpdateView):
    pass
