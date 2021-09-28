from django.forms import ModelForm, ImageField

from taggit.forms import TagField

from apps.core.widgets import SemanticImageFileInput, SemanticTagDropdownWidgetInput

from .models import Post


class EditPostForm(ModelForm):
    feed_cover = ImageField(required=True, widget=SemanticImageFileInput)
    tags = TagField(widget=SemanticTagDropdownWidgetInput(allow_additions=True))

    class Meta:
        fields = ('feed_cover', 'title', 'category', 'feed_article_preview', 'text', 'tags')
        model = Post
