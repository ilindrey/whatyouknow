from django.forms import ModelForm, ImageField

from apps.core.widgets import SemanticImageFileInput

from .models import Post


class EditPostForm(ModelForm):
    feed_cover = ImageField(required=True, widget=SemanticImageFileInput)

    class Meta:
        fields = ('feed_cover', 'title', 'category', 'feed_article_preview', 'text', 'tags')
        model = Post
