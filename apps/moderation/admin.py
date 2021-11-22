from django.contrib import admin
from django.utils.translation import ugettext as _

from .forms import ModeratedObjectForm
from .models import ModeratedObjectMixin
from .constants import (MODERATION_DRAFT_STATE, MODERATION_PENDING_STATE, MODERATION_MODERATED_STATE,
                        MODERATION_APPROVAL_REJECTED, MODERATION_APPROVAL_APPROVED)


class StatusListFilter(admin.SimpleListFilter):
    title = 'Status moderation'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (('draft', _('Draft')),
                ('pending', _('Pending')),
                ('rejected', _('Rejected')),
                ('not_published', _('Approved. Not published')),
                ('published', _('Approved. Published')),
                )

    def queryset(self, request, queryset):
        match self.value():
            case 'draft':
                return queryset.filter(state=MODERATION_DRAFT_STATE)
            case 'pending':
                return queryset.filter(state=MODERATION_PENDING_STATE)
            case 'rejected':
                return queryset.filter(state=MODERATION_MODERATED_STATE, approval=MODERATION_APPROVAL_REJECTED)
            case 'not_published':
                return queryset.filter(state=MODERATION_MODERATED_STATE, approval=MODERATION_APPROVAL_APPROVED,
                                       published=False)
            case 'published':
                return queryset.filter(state=MODERATION_MODERATED_STATE, approval=MODERATION_APPROVAL_APPROVED,
                                       published=True)


class ModeratedObjectAdmin(admin.ModelAdmin):
    form = ModeratedObjectForm
    status_filter_at_the_end = False

    def get_fields(self, request, obj=None, **kwargs):

        fields = super().get_fields(request, obj, **kwargs)
        model_fields = ModeratedObjectMixin._meta.fields

        # if the object is not saved as a draft, we will remove the ability to save as draft
        if obj and obj.state != MODERATION_DRAFT_STATE:
            fields.remove('draft')

        # if the object is new or it is in the draft state, remove the moderation option
        if obj is None or obj.state == MODERATION_DRAFT_STATE:
            for f in model_fields:
                if f.name in fields and f.editable:
                    fields.remove(f.name)

        # reordering
        for f in model_fields:
            if f.name in fields and f.editable:
                fields.remove(f.name)
                fields.append(f.name)

        if 'draft' in fields:
            fields.remove('draft')
            fields.append('draft')

        return fields

    def get_list_filter(self, request):
        list_filter = list(super().get_list_filter(request))
        if self.status_filter_at_the_end:
            list_filter.append(StatusListFilter)
        else:
            list_filter.insert(0, StatusListFilter)
        return list_filter

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display += ('status',)
        return list_display

    @admin.display(description='Status moderation')
    def status(self, instance):
        if instance.state == MODERATION_DRAFT_STATE:
            return _('Draft')
        elif instance.state == MODERATION_PENDING_STATE:
            return _('Pending')
        elif instance.state == MODERATION_MODERATED_STATE \
                and instance.approval == MODERATION_APPROVAL_REJECTED:
            return _('Rejected')
        elif instance.state == MODERATION_MODERATED_STATE \
                and instance.approval == MODERATION_APPROVAL_APPROVED and instance.published is False:
            return _('Approved. Not published')
        elif instance.state == MODERATION_MODERATED_STATE \
                and instance.approval == MODERATION_APPROVAL_APPROVED and instance.published is True:
            return _('Approved. Published')

    class Media:
        js = ('moderation/js/moderated_object_admin.js',)
