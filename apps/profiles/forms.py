from django import forms
# from django.forms.widgets import

from apps.blog.models import CategoryTypes
from apps.core.widgets import SemanticCheckboxSelectMultiple, SemanticSearchInput

from .models import Profile
from .widgets import AvatarFileInput


CATEGORY_CHOICES = CategoryTypes.get_list()


class AvatarForm(forms.ModelForm):
    avatar = forms.ImageField(label='', required=False, widget=AvatarFileInput)

    class Meta:
        model = Profile
        fields = ('avatar', )


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name', 'username', 'email', 'specialization', 'description')


class FeedForm(forms.Form):
    categories = forms.MultipleChoiceField(choices=CATEGORY_CHOICES,
                                           widget=SemanticCheckboxSelectMultiple(inline=True, type_checkbox='toggle'))
    exclude_tags = forms.CharField(widget=SemanticSearchInput(attrs={'placeholder': 'Search tag...'}))
