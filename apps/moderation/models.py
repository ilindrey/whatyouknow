# from django.db import models
# from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.models import ContentType
# from django.utils.translation import ugettext_lazy as _
#
# # from .constants import (MODERATION_DRAFT_STATE, MODERATION_READY_STATE, MODERATION_STATUS_APPROVED,
# #                         MODERATION_STATUS_PENDING, MODERATION_STATUS_REJECTED)
#
# STATUS_CHOICES = [
#     (0, _('Draft')),
#     (1, _('Rejected')),
#     (2, _('Approved')),
#     (3, _('Pending')),
# ]
#
#
# class ModeratedObject(models.Model):
#     content_type = models.ForeignKey(ContentType, null=True, blank=True,
#                                      on_delete=models.SET_NULL,
#                                      editable=False)
#     object_id = models.PositiveIntegerField(null=True, blank=True,
#                                             editable=False, db_index=True)
#     content_object = GenericForeignKey(ct_field='content_type',
#                                        fk_field='object_id')
#     created = models.DateTimeField(auto_now_add=True, editable=False)
#     updated = models.DateTimeField(auto_now=True)
#     status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=0, null=True, blank=True)
#     # changed_object = models.JSONField()
