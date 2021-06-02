from django import forms

from apps.core.widgets import SemanticCheckboxSelectMultiple, SemanticSearchInput
from apps.blog.models import CategoryTypes

from .models import Profile
from .widgets import SemanticAvatarFileInput


class EditAvatarForm(forms.ModelForm):
    avatar = forms.ImageField(label='', required=False, widget=SemanticAvatarFileInput)

    class Meta:
        model = Profile
        fields = ('avatar', )


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name', 'username', 'email', 'specialization', 'description')


class FeedSettingsForm(forms.ModelForm):
    categories = forms.TypedMultipleChoiceField(required=False,
                                                choices=CategoryTypes.get_list(),
                                                coerce=lambda x: int(x),
                                                widget=SemanticCheckboxSelectMultiple(inline=True,
                                                                                      type_checkbox='toggle'))
    search_tags = forms.CharField(label='Exclude tags',
                                  required=False,
                                  widget=SemanticSearchInput(attrs={
                                      'placeholder': 'Search tag...',
                                      }))

    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        keep_fields = ['categories', 'search_tags']
        for key in list(self.fields):
            if key not in keep_fields:
                del self.fields[key]

    def save(self, commit=True):

        # categories
        categories = self.cleaned_data['categories']
        if categories:
            self.instance.settings['feed_categories'] = self.cleaned_data['categories']
        else:
            del self.instance.settings['feed_categories']

        # search_tags
        tag = self.cleaned_data['search_tags']
        if tag:
            self.instance.excluded_feed_tags.add(tag)

        super().save(commit)


