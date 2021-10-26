from django.apps import apps
from django.urls import reverse

from .models import Comment
from .forms import EditCommentForm


class ContentTypeObjectCommentMixin:

    def get(self, request, *args, **kwargs):
        self.content_type_object = self.get_content_type_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.content_type_object = self.get_content_type_object()
        return super().post(request, *args, **kwargs)

    def get_content_type_object(self):
        app_label = self.request.GET.get('app_label') or self.request.POST.get('app_label')
        model_name = self.request.GET.get('model_name') or self.request.POST.get('model_name')
        model_pk = self.request.GET.get('model_pk') or self.request.POST.get('model_pk')
        return apps.get_model(app_label, model_name).objects.get(pk=model_pk)

    def get_query_string(self):
        app_label = self.content_type_object._meta.app_label
        model_name = self.content_type_object._meta.model_name
        model_pk = self.content_type_object.pk
        return f'?app_label={app_label}&model_name={model_name}&model_pk={model_pk}'


class CreateUpdateCommentMixin(ContentTypeObjectCommentMixin):
    form_class = EditCommentForm
    model = Comment
    template_name = 'comments/edit.html'

    def get_success_url(self):
        return reverse('comment_list') + self.get_query_string()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'action_url': self.request.GET.get('action_url') or self.request.POST.get('action_url'),
            'action_type': self.request.GET.get('action_type') or self.request.POST.get('action_type'),
            'target_id': self.request.GET.get('target_id') or self.request.POST.get('target_id')
            })
        return context
