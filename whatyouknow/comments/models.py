from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django_summernote.fields import SummernoteTextField
from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, blank=False, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = SummernoteTextField()
    posted = models.DateTimeField(default=timezone.now, editable=False)
    edited = models.DateTimeField(auto_now=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['posted']