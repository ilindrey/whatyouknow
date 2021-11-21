
from .constants import (MODERATION_DRAFT_STATE, MODERATION_PENDING_STATE, MODERATION_MODERATED_STATE,
                        MODERATION_APPROVAL_REJECTED, MODERATION_APPROVAL_APPROVED)


def save_as_draft(sender, instance, **kwargs):
    instance.state = MODERATION_DRAFT_STATE
    instance.approval = None
    instance.published = False


def save_as_pending(sender, instance, **kwargs):
    instance.state = MODERATION_PENDING_STATE
    instance.approval = None
    instance.published = False


def save_as_rejected(sender, instance, **kwargs):
    instance.state = MODERATION_MODERATED_STATE
    instance.approval = MODERATION_APPROVAL_REJECTED
    instance.published = False
    instance.reason = kwargs.get('reason')


def save_as_not_published(sender, instance, **kwargs):
    instance.state = MODERATION_MODERATED_STATE
    instance.approval = MODERATION_APPROVAL_APPROVED
    instance.published = False
    instance.reason = kwargs.get('reason')


def save_as_published(sender, instance, **kwargs):
    instance.state = MODERATION_MODERATED_STATE
    instance.approval = MODERATION_APPROVAL_APPROVED
    instance.published = True
