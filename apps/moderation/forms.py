from django.forms import ModelForm, RadioSelect, ChoiceField
from .mixins import ModeratedObjectMixin, STATE_CHOICES


class ModeratedObjectForm(ModelForm):
    # state = ChoiceField(choices=STATE_CHOICES, widget=RadioSelect)

    class Meta:
        model = ModeratedObjectMixin
        fields = '__all__'
        widgets = {
            # 'state': RadioSelect,
            'approval': RadioSelect
            }
