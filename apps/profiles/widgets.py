from django.forms.widgets import ClearableFileInput
from django.templatetags.static import static

from easy_thumbnails.templatetags.thumbnail import thumbnail_url


class SemanticAvatarFileInput(ClearableFileInput):
    initial_text = 'Change avatar'
    template_name = 'widgets/avatar_file_input.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        value = context['widget']['value']
        if value:
            avatar_img = thumbnail_url(value, 'card')
        else:
            avatar_img = static('profiles/image/avatar_placeholder.svg')

        context['widget'].update({
            'avatar_img': avatar_img,
            })
        return context
