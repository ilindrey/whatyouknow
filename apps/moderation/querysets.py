
from django.db.models import QuerySet, BooleanField, Q, Case, When, Value
from mptt.querysets import TreeQuerySet

from .constants import (MODERATION_DRAFT_STATE, MODERATION_PENDING_STATE, MODERATION_MODERATED_STATE,
                        MODERATION_APPROVAL_REJECTED, MODERATION_APPROVAL_APPROVED)


class ModeratedQuerySetMixin:

    def drafts(self):
        clone = self._chain()
        return clone.filter(state=MODERATION_DRAFT_STATE)

    def pending(self):
        clone = self._chain()
        return clone.filter(state=MODERATION_PENDING_STATE)

    def moderated(self):
        clone = self._chain()
        return clone.filter(state=MODERATION_MODERATED_STATE)

    def rejected(self):
        clone = self._chain()
        return clone.filter(state=MODERATION_MODERATED_STATE, approval=MODERATION_APPROVAL_REJECTED)

    def approved(self):
        clone = self._chain()
        return clone.filter(state=MODERATION_MODERATED_STATE, approval=MODERATION_APPROVAL_APPROVED)


class ModeratedQuerySet(ModeratedQuerySetMixin, QuerySet):
    pass


class ModeratedTreeQuerySet(ModeratedQuerySetMixin, TreeQuerySet):
    pass
