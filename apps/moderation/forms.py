from django.forms import ModelForm, RadioSelect, BooleanField
from django.utils.translation import ugettext_lazy as _

from .constants import MODERATION_DRAFT_STATE, MODERATION_PENDING_STATE
from .models import ModeratedObjectMixin


class ModeratedObjectForm(ModelForm):
    draft = BooleanField(label=_('Save as draft'), initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(ModeratedObjectForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.state != MODERATION_DRAFT_STATE:
            if 'draft' in self.fields.keys():
                self.fields.pop('draft')

    def save(self, commit=True):
        draft = self.cleaned_data.get('draft')
        if draft is not None:
            self.instance.state = MODERATION_DRAFT_STATE if draft else MODERATION_PENDING_STATE
        return super().save(commit)

    class Meta:
        model = ModeratedObjectMixin
        fields = '__all__'
        labels = {
            'published': _('Publish')
            }
        widgets = {
            'approval': RadioSelect
            }
