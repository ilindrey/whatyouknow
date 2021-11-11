from django.forms import ModelForm, RadioSelect
from .mixins import ModeratedObjectMixin


class ModeratedObjectForm(ModelForm):
    class Meta:
        model = ModeratedObjectMixin
        fields = '__all__'
        widgets = {'status': RadioSelect}