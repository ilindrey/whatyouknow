from django.forms import ModelForm

from .models import Profile

# from .widgets import AvatarFileInput


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', )
        # widgets = {
        #     'avatar': CroppieField()
        #     }


# class AvatarForm(ModelForm):
#     avatar = CroppieField()
#
#     class Meta:
#         model = Profile
#         fields = ('avatar',)
