
from django.db.models import Manager
from mptt.managers import TreeManager

from .querysets import ModeratedQuerySet, ModeratedTreeQuerySet


class ModeratedManager(Manager.from_queryset(ModeratedQuerySet)):
    pass


class ModeratedTreeManager(TreeManager.from_queryset(ModeratedTreeQuerySet)):
    pass
