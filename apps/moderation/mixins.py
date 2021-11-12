from django.db import models
from django.utils.translation import ugettext_lazy as _

from .constants import (MODERATION_DRAFT_STATE, MODERATION_PENDING_STATE, MODERATION_MODERATED_STATE,
                        MODERATION_APPROVAL_REJECTED, MODERATION_APPROVAL_APPROVED)


STATE_CHOICES = [
    (MODERATION_DRAFT_STATE, _('Draft')),
    (MODERATION_PENDING_STATE, _('Pending')),
    (MODERATION_MODERATED_STATE, _('Moderated')),
]

APPROVAL_CHOICES = [
    (MODERATION_APPROVAL_APPROVED, _('Approved')),
    (MODERATION_APPROVAL_REJECTED, _('Rejected')),
]


class ModeratedObjectMixin(models.Model):
    state = models.PositiveIntegerField(choices=STATE_CHOICES, default=MODERATION_DRAFT_STATE,
                                        null=False, blank=False)
    approval = models.PositiveIntegerField(choices=APPROVAL_CHOICES, default=None, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if self.state == MODERATION_DRAFT_STATE:
            self.approval = None
            self.reason = None
        else:
            self.state = MODERATION_MODERATED_STATE if self.approval else MODERATION_PENDING_STATE
            self.reason = self.reason if self.approval == MODERATION_APPROVAL_REJECTED else None

        super().save(*args, **kwargs)
