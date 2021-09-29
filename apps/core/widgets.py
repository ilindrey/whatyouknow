from django.forms.widgets import TextInput, Select, SelectMultiple, CheckboxSelectMultiple, ClearableFileInput
from django.templatetags.static import static

from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from taggit.forms import TagWidget
from taggit.models import Tag

from .utils import js_bool_format


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


class SemanticTagDropdownWidgetInput(TagWidget):
    template_name = 'widgets/tag_dropdown_input.html'
    model = Tag

    class Media:
        js = ('widgets/js/tag_dropdown_input.js', )

    def __init__(self, attrs=None, model=None, default_text='Search tags...', allow_additions=False, clearable=True):
        super().__init__(attrs)
        self.model = model or self.model
        self.default_text = default_text
        self.allow_additions = allow_additions
        self.clearable = clearable

    def get_tag_list(self):
        queryset = self.model._default_manager.all()
        return [{'icon': 'tag', 'value': obj.name, 'name': obj.name, 'text': obj.name} for obj in queryset]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'default_text': self.default_text,
            'allow_additions': self.allow_additions,
            'clearable': self.clearable,
            'tag_list': self.get_tag_list(),
            'autocomplete': False,
            })
        return context


class SemanticSelectDropdown(Select):

    class Media:
        js = ('widgets/js/select_dropdown.js', )

    def __init__(self, attrs=None, search=True, clearable=True, placeholder='Search...'):
        params = {
            'semantic': 'dropdown',
            'data-search': js_bool_format(search),
            'data-allow-additions': js_bool_format(False),
            'data-clearable': js_bool_format(clearable),
            'data-placeholder': placeholder
            }
        if attrs:
            attrs.updata(params)
        else:
            attrs = params
        super().__init__(attrs)


class SemanticSelectMultipleDropdown(SemanticSelectDropdown, SelectMultiple):
    pass


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
            'type_checkbox': self.type_checkbox,
            })
        return context


class SemanticImageFileInput(ClearableFileInput):
    initial_text = 'Change image'
    template_name = 'widgets/image_file_input.html'

    class Media:
        js = ('widgets/js/image_file_input.js', )

    def __init__(self,
                 attrs=None,
                 img_size='medium',
                 img_type=None,  # circular or rounded
                 img_extra_class=None,
                 thumbnail_size='default',
                 placeholder='widgets/images/image_file_input_placeholder.svg'):
        super().__init__(attrs)
        self.img_size = img_size
        self.img_type = img_type
        self.img_extra_class = img_extra_class
        self.thumbnail_size = thumbnail_size
        self.placeholder = static(placeholder)

    def is_initial(self, value):
        return bool(value)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        img_url = None
        value = context['widget']['value']
        if value:
            img_url = thumbnail_url(value, self.thumbnail_size)

        if not img_url:
            img_url = self.placeholder

        context['widget'].update({
            'img_url': img_url,
            'img_size': self.img_size,
            'img_type': self.img_type,
            'img_extra_class': self.img_extra_class,
            'is_initial': self.is_initial(self.initial_text),
            'placeholder': self.placeholder,
            })
        return context

