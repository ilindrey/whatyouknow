from django.db.models import Manager

from .constants import (MODERATION_DRAFT_STATE, MODERATION_PENDING_STATE, MODERATION_MODERATED_STATE,
                        MODERATION_APPROVAL_REJECTED, MODERATION_APPROVAL_APPROVED)


class ModeratedManager(Manager):

    def drafts(self):
        return self.get_queryset().filter(state=MODERATION_DRAFT_STATE)

    def pending(self):
        return self.get_queryset().filter(state=MODERATION_PENDING_STATE)

    def moderated(self):
        return self.get_queryset().filter(state=MODERATION_MODERATED_STATE)

    def rejected(self):
        return self.get_queryset().filter(state=MODERATION_MODERATED_STATE, approval=MODERATION_APPROVAL_REJECTED)

    def approved(self):
        return self.get_queryset().filter(state=MODERATION_MODERATED_STATE, approval=MODERATION_APPROVAL_APPROVED)
