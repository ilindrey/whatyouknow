from django.forms import ModelForm

from .models import Post


class EditPostForm(ModelForm):

    class Meta:
        fields = ('title', 'category', 'feed_cover', 'feed_article_preview', 'text', 'tags')
        model = Post

    # def save(self, commit=True):
    #     """If the form is valid, save the associated model."""
    #     self.instance = self.kwargs['user']
    #     return super().save(commit)

    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     return super().__init__(*args, **kwargs)
    #
    # def save(self, commit=True):
    #     self.instance.user = self.user
    #     return super().save(commit)

