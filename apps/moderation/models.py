from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
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
    published = models.BooleanField(_('Published'), default=False, blank=True)
    reason = models.TextField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    date_published = models.DateTimeField(null=True, blank=True, editable=False)

    is_draft = models.BooleanField(default=False, null=False, editable=False)
    is_pending = models.BooleanField(default=False, null=False, editable=False)
    is_moderated = models.BooleanField(default=False, null=False, editable=False)
    is_approved = models.BooleanField(default=False, null=False, editable=False)
    is_rejected = models.BooleanField(default=False, null=False, editable=False)

    edited_by_user = models.BooleanField(default=False, null=False, editable=False)

    objects = ModeratedManager()

    class Meta:
        abstract = True

    def clean(self):
        if (self.approval == MODERATION_APPROVAL_APPROVED and not self.published and not self.reason) \
                or (self.approval == MODERATION_APPROVAL_REJECTED and not self.reason):
            raise ValidationError(message=_('Enter a reason.'), code='invalid', params={'value': self.reason})
        super().clean()

    def save(self, *args, **kwargs):

        if self.approval is not None and self.pk is not None:
            self.state = MODERATION_MODERATED_STATE
        else:
            if self.state in (MODERATION_PENDING_STATE, MODERATION_MODERATED_STATE):
                self.state = MODERATION_PENDING_STATE
            else:
                self.state = MODERATION_DRAFT_STATE

        self.is_draft = self.state == MODERATION_DRAFT_STATE
        self.is_pending = self.state == MODERATION_PENDING_STATE
        self.is_moderated = self.state == MODERATION_MODERATED_STATE

        self.is_approved = self.is_moderated and self.approval == MODERATION_APPROVAL_APPROVED
        self.is_rejected = self.is_moderated and self.approval == MODERATION_APPROVAL_REJECTED

        if not self.is_moderated:
            self.approval = None

        if not self.is_approved:
            self.published = False

        if not self.is_rejected and not (self.is_approved and not self.published):
            self.reason = None

        if self.is_approved and self.published and self.date_published is None:
            self.date_published = now()

        super().save(*args, **kwargs)

    def save_as_draft(self, *args, **kwargs):
        self.state = MODERATION_DRAFT_STATE
        self.approval = None
        self.save(*args, **kwargs)

    def save_as_pending(self,*args, **kwargs):
        self.state = MODERATION_PENDING_STATE
        self.approval = None
        self.save(*args, **kwargs)

    def save_as_approved(self, *args, **kwargs):
        self.state = MODERATION_MODERATED_STATE
        self.approval = MODERATION_APPROVAL_APPROVED
        self.save(*args, **kwargs)

    def save_as_rejected(self, reason=None, *args, **kwargs):
        self.state = MODERATION_MODERATED_STATE
        self.approval = MODERATION_APPROVAL_REJECTED
        self.reason = reason
        self.save(*args, **kwargs)

    def save_as_published(self, *args, **kwargs):
        self.state = MODERATION_MODERATED_STATE
        self.approval = MODERATION_APPROVAL_APPROVED
        self.published = True
        self.save(*args, **kwargs)

