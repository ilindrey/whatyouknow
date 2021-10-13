from django.forms import Form, CharField

from .widgets import SemanticSearchInput


class SearchForm(Form):
    query = CharField(label='',
                      required=False,
                      widget=SemanticSearchInput(extra_class='fluid',
                                                 attrs={'placeholder': 'Enter text, category or tag to search...'}))
