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


class BaseCommentList(generic.ListView):
    allow_empty = True
    template_name = 'comments/list.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['is_parent'] = self.request.GET.get('parent_id') is None
        return context


class ParentCommentList(MultipleObjectCommentsMixin, BaseCommentList):
    paginate_by = 100

    def get_queryset(self):
        return super().get_queryset().filter(parent=None)


class DescendantCommentList(BaseCommentList):

    def get_queryset(self):
        parent_id = self.request.GET.get('parent_id')
        return Comment.objects.get(pk=parent_id).get_descendants()