from django import forms
from django.utils.translation import gettext_lazy as _

from taggit.forms import TagField

from apps.core.widgets import SemanticImageFileInput, SemanticTagDropdownWidgetInput

from .models import Post


class EditPostForm(forms.ModelForm):
    feed_cover = forms.ImageField(label=_('Feed cover'), required=True, widget=SemanticImageFileInput)
    tags = TagField(label=_('Tags'), widget=SemanticTagDropdownWidgetInput(allow_additions=True))

    class Meta:
        fields = ('feed_cover', 'title', 'category', 'feed_article_preview', 'text', 'tags')
        model = Post
