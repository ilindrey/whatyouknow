from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django_summernote.fields import SummernoteTextField
from mptt.models import MPTTModel, TreeForeignKey

from ..core.mixins import TimeStampsMixin
from ..moderation.managers import ModeratedTreeManager
from ..moderation.models import BaseModeratedObject


class Comment(TimeStampsMixin, BaseModeratedObject, MPTTModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, blank=False, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = SummernoteTextField()
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            related_name='children',
                            editable=False)

    objects = ModeratedTreeManager()

    class MPTTMeta:
        order_insertion_by = ['created']

    def get_absolute_url(self):
        return self.content_object.get_absolute_url() + '?comment=' + str(self.pk)
