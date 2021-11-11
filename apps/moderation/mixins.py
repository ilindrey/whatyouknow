from django.db import models
from django.utils.translation import ugettext_lazy as _

# from .constants import MODERATION_DRAFT_STATE, MODERATION_READY_STATE
from .constants import (MODERATION_STATUS_DRAFT, MODERATION_STATUS_PENDING, MODERATION_STATUS_APPROVED,
                        MODERATION_STATUS_REJECTED)

# STATE_CHOICES = [
#     (MODERATION_DRAFT_STATE, _('Draft')),
#     (MODERATION_READY_STATE, _('Ready for moderation')),
# ]


STATUS_CHOICES = [
    (MODERATION_STATUS_DRAFT, _('Draft')),
    (MODERATION_STATUS_PENDING, _('Pending')),
    (MODERATION_STATUS_APPROVED, _('Approved')),
    (MODERATION_STATUS_REJECTED, _('Rejected')),
]


class ModeratedObjectMixin(models.Model):
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=MODERATION_STATUS_PENDING,
                                         null=True, blank=False)
    reason = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


