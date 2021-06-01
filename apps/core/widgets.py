from django.forms.widgets import CheckboxSelectMultiple, TextInput


class SemanticCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = 'widgets/checkbox_select.html'
    option_template_name = 'widgets/checkbox_option.html'
    inline = False
    type_checkbox = None

    def __init__(self, inline=False, type_checkbox=None):
        super().__init__()
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
