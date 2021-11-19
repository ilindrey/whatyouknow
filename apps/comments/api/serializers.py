from rest_framework.serializers import ModelSerializer
from taggit_serializer.serializers import TaggitSerializer

from ..models import Comment


class CommentSerializer(TaggitSerializer, ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
