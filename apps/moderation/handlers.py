
from .constants import (MODERATION_DRAFT_STATE, MODERATION_PENDING_STATE, MODERATION_MODERATED_STATE,
                        MODERATION_APPROVAL_REJECTED, MODERATION_APPROVAL_APPROVED)


def save_as_draft(sender, instance, **kwargs):
    instance.state = MODERATION_DRAFT_STATE


def save_as_pending(sender, instance, **kwargs):
    instance.state = MODERATION_PENDING_STATE


def save_as_approved(sender, instance, **kwargs):
    instance.state = MODERATION_MODERATED_STATE
    instance.approval = MODERATION_APPROVAL_APPROVED


def save_as_rejected(sender, instance, **kwargs):
    instance.state = MODERATION_MODERATED_STATE
    instance.approval = MODERATION_APPROVAL_REJECTED
    instance.reason = kwargs.get('reason')
