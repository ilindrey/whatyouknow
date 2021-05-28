from django.forms.widgets import CheckboxSelectMultiple, TextInput


class SemanticCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = 'widgets/checkbox_select.html'
    option_template_name = 'widgets/checkbox_option.html'


class SemanticSearchInput(TextInput):
    template_name = 'widgets/search.html'
