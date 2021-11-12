from django.contrib import admin

from .forms import ModeratedObjectForm


class ModeratedObjectAdmin(admin.ModelAdmin):
    form = ModeratedObjectForm
    moderating_form_template = None
    readonly_fields = ('state',)

    def get_fields(self, request, obj=None, **kwargs):
        fields = super().get_fields(request, obj, **kwargs)

        from apps.moderation.mixins import ModeratedObjectMixin
        for f in ModeratedObjectMixin._meta.fields:
            if f.editable:
                fields.remove(f.name)
                fields.append(f.name)
        return fields

    class Media:
        # css = {
        #     "all": ("my_styles.css",)
        #     }
        js = ('moderation/js/moderated_object_admin.js', )