from django import forms
from django.contrib.auth.forms import SetPasswordForm, UsernameField
from django.utils.translation import gettext_lazy as _

from taggit.models import Tag

from apps.core.widgets import SemanticCheckboxSelectMultiple, SemanticSelectMultipleDropdown, SemanticImageFileInput
from apps.blog.models import CategoryTypes

from .models import Profile


class EditProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='',
                              required=False,
                              widget=SemanticImageFileInput(
                                  placeholder='profiles/image/avatar_placeholder.svg',
                                  thumbnail_size='small',
                                  img_size='small',
                                  img_type='circular',
                                  ))

    class Meta:
        model = Profile
        fields = ('avatar', 'username', 'email', 'name', 'specialization', 'description')


class EditFeedSettingsForm(forms.ModelForm):
    categories = forms.TypedMultipleChoiceField(label=_('Categories'),
                                                required=False,
                                                choices=CategoryTypes.choices(),
                                                coerce=lambda x: int(x),
                                                widget=SemanticCheckboxSelectMultiple(inline=False,
                                                                                      type_checkbox='toggle'))
    excluded_feed_tags = forms.ModelMultipleChoiceField(label=_('Exclude tags'),
                                                        queryset=Tag.objects.all().order_by('name'),
                                                        required=False,
                                                        widget=SemanticSelectMultipleDropdown(
                                                            placeholder='Search tags...'))

    field_order = ('categories', 'excluded_feed_tags')

    class Meta:
        model = Profile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        keep_fields = ['categories', 'excluded_feed_tags']
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

        super().save(commit)


class RegistrationForm(SetPasswordForm, forms.ModelForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    email = forms.EmailField()

    field_order = ('username', 'email', 'new_password1', 'new_password2')

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        SetPasswordForm.user = self.instance
        del self.fields['password']

    def save(self, commit=True):
        """Save the new password."""
        super().save(commit)
        return self.instance
