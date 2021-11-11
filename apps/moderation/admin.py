from django.contrib import admin

from .forms import ModeratedObjectForm


class ModeratedObjectAdmin(admin.ModelAdmin):
    form = ModeratedObjectForm
    # pass

    def get_fields(self, request, obj=None, **kwargs):
        fields = super().get_fields(request, obj, **kwargs)

        from apps.moderation.mixins import ModeratedObjectMixin
        for field in ModeratedObjectMixin._meta.fields:
            fields.remove(field.name)
            fields.append(field.name)
        return fields
