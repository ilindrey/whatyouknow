
from django.urls import reverse
from django.db import models
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django_summernote.fields import SummernoteTextField
from mptt.models import MPTTModel, TreeForeignKey

from apps_packages.summernote.validators import SummernoteMinValueValidator
from ..moderation.managers import ModeratedTreeManager
from ..moderation.models import BaseModeratedObject


class Comment(BaseModeratedObject, MPTTModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = SummernoteTextField(validators=[SummernoteMinValueValidator(10)])
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children',
                            editable=False)

    objects = ModeratedTreeManager()

    class MPTTMeta:
        order_insertion_by = ['date_created']

    def get_absolute_url(self):
        return self.content_object.get_absolute_url() + '?comment=' + str(self.pk)

    def get_admin_url(self):
        url = admin_urlname(self._meta, 'change')
        return reverse(url, args=(self.pk,))
