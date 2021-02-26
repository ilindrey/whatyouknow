from django.apps import apps
from django.views import generic
from django.contrib.contenttypes.models import ContentType


from .models import Comment


class CommentList(generic.ListView):
    allow_empty = False

    def get_queryset(self):

        parent_id = self.request.GET.get('parent_id')

        app_label = self.request.GET.get('app_label')
        model_name = self.request.GET.get('model_name')
        model_pk = self.request.GET.get('model_pk')

        obj = apps.get_model(app_label, model_name).objects.get(pk=model_pk)

        return Comment.objects.filter(content_type=ContentType.objects.get_for_model(obj._meta.model),
                                      object_id=obj.pk,
                                      parent=parent_id)


class CommentParentsList(CommentList):
    paginate_by = 10
    template_name = 'comments/parent_list.html'


class CommentChildrenList(CommentList):
    template_name = 'comments/children_list.html'
