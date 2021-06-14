from django.apps import apps
from django.views import generic
from django.contrib.contenttypes.models import ContentType

from .models import Comment


class MultipleObjectCommentsMixin:

    def get_queryset(self):
        app_label = self.request.GET.get('app_label')
        model_name = self.request.GET.get('model_name')
        model_pk = self.request.GET.get('model_pk')

        obj = apps.get_model(app_label, model_name).objects.get(pk=model_pk)

        return Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj._meta.model),
                                      object_id=obj.pk)


class CommentList(MultipleObjectCommentsMixin, generic.ListView):
    template_name = 'comments/list.html'

    def get_queryset(self):
        return super().get_queryset()

