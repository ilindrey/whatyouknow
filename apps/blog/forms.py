from django.forms import ModelForm

from .models import Post


class PostWriteForm(ModelForm):

    class Meta:
        fields = ('title', 'category', 'feed_cover', 'feed_article_preview', 'text', 'tags')
        model = Post
