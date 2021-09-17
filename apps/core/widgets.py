from django.forms.widgets import TextInput, CheckboxSelectMultiple, ClearableFileInput
from django.templatetags.static import static

from easy_thumbnails.templatetags.thumbnail import thumbnail_url


class SemanticSearchInput(TextInput):
    template_name = 'widgets/search.html'

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if self.attrs is None:
            self.attrs = {'class': 'prompt'}
        elif 'class' not in self.attrs:
            self.attrs['class'] = 'prompt'
        elif 'prompt' not in self.attrs['class']:
            self.attrs['class'] += ' prompt'


class SemanticCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = 'widgets/checkbox_select.html'
    option_template_name = 'widgets/checkbox_option.html'

    def __init__(self, attrs=None, choices=(), inline=False, type_checkbox=None):
        super().__init__(attrs, choices)
        self.inline = inline
        self.type_checkbox = type_checkbox

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'inline': self.inline,
            'type_checkbox': self.type_checkbox
            })
        return context


class SemanticImageFileInput(ClearableFileInput):
    initial_text = 'Change image'
    template_name = 'widgets/image_file_input.html'

    def __init__(self,
                 attrs=None,
                 placeholder='widgets/images/image_file_input_placeholder.svg',
                 thumbnail_size='default',
                 img_size='medium',
                 img_type=None,  # circular
                 img_extra_class=None):
        super().__init__(attrs)
        self.placeholder = placeholder
        self.thumbnail_size = thumbnail_size
        self.img_size = img_size
        self.img_type = img_type
        self.img_extra_class = img_extra_class

    def is_initial(self, value):
        return bool(value)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        image_img = None
        value = context['widget']['value']
        if value:
            image_img = thumbnail_url(value, self.thumbnail_size)

        if not image_img:
            image_img = static(self.placeholder)

        context['widget'].update({
            'image_img': image_img,
            'is_initial': self.is_initial(self.initial_text),
            'img_size': self.img_size,
            'img_type': self.img_type,
            'img_extra_class': self.img_extra_class,
            })
        return context
