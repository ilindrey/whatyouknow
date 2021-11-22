from .constants import MODERATION_MODERATED_STATE


class SetEditedByUserMixin:

    def form_valid(self, form):
        if form.instance.state == MODERATION_MODERATED_STATE and not form.instance.edited_by_user:
            form.instance.edited_by_user = True
        return super().form_valid(form)
