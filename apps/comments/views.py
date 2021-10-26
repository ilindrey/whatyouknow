from django.views import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Comment
from .mixins import ContentTypeObjectCommentMixin, CreateUpdateCommentMixin


class CommentListView(ContentTypeObjectCommentMixin, generic.ListView):
    model = Comment
    template_name = 'comments/list.html'

    def get_queryset(self):
        return super().get_queryset()\
            .filter(content_type=ContentType.objects.get_for_model(self.content_type_object._meta.model),
                    object_id=self.content_type_object.pk)


class CreateCommentView(CreateUpdateCommentMixin, LoginRequiredMixin, generic.CreateView):

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.content_type = ContentType.objects.get_for_model(self.content_type_object._meta.model)
        form.instance.object_id = self.content_type_object.pk
        if 'reply' in self.request.POST.get('action_type'):
            form.instance.parent_id = self.request.POST.get('target_id')
        return super().form_valid(form)


class EditCommentView(CreateUpdateCommentMixin, LoginRequiredMixin, generic.UpdateView):
    pass
