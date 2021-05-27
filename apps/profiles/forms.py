from django import forms

from .models import Profile

from .widgets import AvatarFileInput


class AvatarForm(forms.ModelForm):
    avatar = forms.ImageField(label='', required=False, widget=AvatarFileInput)

    class Meta:
        model = Profile
        fields = ('avatar', )


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name', 'username', 'email', 'specialization', 'description')
