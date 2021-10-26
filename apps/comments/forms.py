from django.forms import ModelForm, CharField

from django_summernote.widgets import SummernoteWidget

from .models import Comment


class EditCommentForm(ModelForm):
    text = CharField(label='', widget=SummernoteWidget(attrs={'summernote': {'height': '250px'}}))

    class Meta:
        model = Comment
        fields = ('text', )
