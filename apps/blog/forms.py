from django import forms
from django.utils.translation import gettext_lazy as _

from django_summernote.widgets import SummernoteWidget
from taggit.forms import TagField

from ..core.widgets import SemanticImageFileInput, SemanticTagDropdownWidgetInput
from ..moderation.forms import ModeratedObjectForm
from .models import Post


PREVIEW_CONFIG = {'summernote':
                  {
                      'height': '150',
                      'toolbar': [],
                  }
                  }


class EditPostForm(forms.ModelForm):
    feed_cover = forms.ImageField(label=_('Feed cover'), required=True, widget=SemanticImageFileInput)
    tags = TagField(label=_('Tags'), widget=SemanticTagDropdownWidgetInput(allow_additions=True))
    feed_article_preview = forms.CharField(label=_('Feed article preview'),
                                           widget=SummernoteWidget(attrs=PREVIEW_CONFIG))

    class Meta:
        fields = ('feed_cover', 'title', 'category', 'feed_article_preview', 'text', 'tags')
        model = Post


class EditPostAdminForm(ModeratedObjectForm):
    feed_article_preview = forms.CharField(label=_('Feed article preview'),
                                           widget=SummernoteWidget(attrs=PREVIEW_CONFIG))

    class Meta(ModeratedObjectForm.Meta):
        model = Post
