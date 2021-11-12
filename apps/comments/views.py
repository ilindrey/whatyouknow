from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Comment
from .mixins import ContentTypeObjectCommentMixin, CreateUpdateCommentMixin


class CommentListView(ContentTypeObjectCommentMixin, generic.ListView):
    model = Comment
    template_name = 'comments/list.html'

    def get_queryset(self):
        return self.model.objects.approved()\
            .filter(content_type=self.content_type,
                    object_id=self.ct_object.pk)


class CreateCommentView(CreateUpdateCommentMixin, LoginRequiredMixin, generic.CreateView):

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.content_type = self.content_type
        form.instance.object_id = self.ct_object.pk
        if 'reply' in self.request.POST.get('action_type'):
            form.instance.parent_id = self.request.POST.get('target_id')
        return super().form_valid(form)


class EditCommentView(CreateUpdateCommentMixin, LoginRequiredMixin, generic.UpdateView):
    pass
