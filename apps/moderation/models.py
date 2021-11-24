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


class ModeratedObjectMixin(models.Model):
    state = models.PositiveIntegerField(_('State'), choices=STATE_CHOICES, default=MODERATION_DRAFT_STATE,
                                        null=False, blank=False, editable=False)
    approval = models.PositiveIntegerField(
        _('Approval'), choices=APPROVAL_CHOICES, default=None, null=True, blank=True)
    published = models.BooleanField(_('Published'), default=False, blank=True)
    reason = models.TextField(_('Reason'), null=True, blank=True)

    date_created = models.DateTimeField(
        _('Date created'), default=now, null=False, blank=False, editable=False)
    date_updated = models.DateTimeField(
        _('Date updated'), default=now, null=False, blank=False, editable=False)
    date_published = models.DateTimeField(
        _('Date published'), null=True, blank=True, editable=False)

    is_draft = models.BooleanField(
        _('Is draft'), default=False, null=False, editable=False)
    is_pending = models.BooleanField(
        _('Is pending'), default=False, null=False, editable=False)
    is_moderated = models.BooleanField(
        _('Is moderated'), default=False, null=False, editable=False)
    is_approved = models.BooleanField(
        _('Is approved'), default=False, null=False, editable=False)
    is_rejected = models.BooleanField(
        _('Is rejected'), default=False, null=False, editable=False)

    edited_by_user = models.BooleanField(
        _('Edited by user'), default=False, null=False, editable=False)

    objects = ModeratedManager()

    class Meta:
        abstract = True

    def clean(self):
        if (self.approval == MODERATION_APPROVAL_APPROVED and not self.published and not self.reason) \
                or (self.approval == MODERATION_APPROVAL_REJECTED and not self.reason):
            raise ValidationError(message=_('Enter a reason.'), code='invalid', params={
                                  'value': self.reason})
        super().clean()

    def save(self, *args, **kwargs):

        keys = kwargs.keys()

        if self.pk is None and self.date_created is None:
            self.date_created = kwargs.get('date_created', now())
        self.date_updated = kwargs.get('date_created', now())

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
            self.date_published = kwargs.get('date_published', now())

        if 'edited_by_user' in keys:
            self.edited_by_user = kwargs.get(
                'edited_by_user', self.edited_by_user)

        clean_keys_list = ['date_created', 'date_updated',
                           'date_published', 'edited_by_user']
        for key in clean_keys_list:
            if key in keys:
                del kwargs[key]

        super().save(*args, **kwargs)

    def save_as_draft(self, *args, **kwargs):
        self.state = MODERATION_DRAFT_STATE
        self.approval = None
        self.published = False
        self.save(*args, **kwargs)

    def save_as_pending(self, *args, **kwargs):
        self.state = MODERATION_PENDING_STATE
        self.approval = None
        self.published = False
        self.save(*args, **kwargs)

    def save_as_rejected(self, reason, *args, **kwargs):
        self.state = MODERATION_MODERATED_STATE
        self.approval = MODERATION_APPROVAL_REJECTED
        self.reason = reason
        self.published = False
        self.save(*args, **kwargs)

    def save_as_not_published(self, reason, *args, **kwargs):
        self.state = MODERATION_MODERATED_STATE
        self.approval = MODERATION_APPROVAL_APPROVED
        self.published = False
        self.reason = reason
        self.save(*args, **kwargs)

    def save_as_published(self, *args, **kwargs):
        self.state = MODERATION_MODERATED_STATE
        self.approval = MODERATION_APPROVAL_APPROVED
        self.published = True
        self.save(*args, **kwargs)
