from django.forms.widgets import CheckboxSelectMultiple, TextInput


class SemanticCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = 'widgets/checkbox_select.html'
    option_template_name = 'widgets/checkbox_option.html'
    inline = False
    type_checkbox = None

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
