from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import ModeratedManager
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


class BaseModeratedObject(models.Model):
    state = models.PositiveIntegerField(choices=STATE_CHOICES, default=MODERATION_DRAFT_STATE,
                                        null=False, blank=False, editable=False)
    approval = models.PositiveIntegerField(choices=APPROVAL_CHOICES, default=None, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)

    is_draft = models.BooleanField(default=False, null=False, editable=False)
    is_pending = models.BooleanField(default=False, null=False, editable=False)
    is_moderated = models.BooleanField(default=False, null=False, editable=False)
    is_approved = models.BooleanField(default=False, null=False, editable=False)
    is_rejected = models.BooleanField(default=False, null=False, editable=False)

    objects = ModeratedManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        self.is_draft = self.state == MODERATION_DRAFT_STATE
        self.is_pending = self.state == MODERATION_PENDING_STATE
        self.is_moderated = self.state == MODERATION_MODERATED_STATE and self.approval is not None

        self.is_approved = self.is_moderated and self.approval == MODERATION_APPROVAL_APPROVED
        self.is_rejected = self.is_moderated and self.approval == MODERATION_APPROVAL_REJECTED

        if not self.is_rejected:
            self.reason = None

        if not self.is_moderated:
            self.approval = None

        super().save(*args, **kwargs)
