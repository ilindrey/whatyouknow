from django import forms

from .models import Profile

from .widgets import AvatarFileInput


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='', required=False, widget=AvatarFileInput)

    class Meta:
        model = Profile
        fields = ('avatar', )