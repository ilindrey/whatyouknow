from django.contrib import admin

from .forms import ModeratedObjectForm
from .models import BaseModeratedObject
from .constants import MODERATION_DRAFT_STATE


class ModeratedObjectAdmin(admin.ModelAdmin):
    form = ModeratedObjectForm

    def get_fields(self, request, obj=None, **kwargs):

        fields = super().get_fields(request, obj, **kwargs)
        model_fields = BaseModeratedObject._meta.fields

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

        return fields

    class Media:
        js = ('moderation/js/moderated_object_admin.js', )