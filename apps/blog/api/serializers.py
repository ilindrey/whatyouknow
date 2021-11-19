from rest_framework.serializers import ModelSerializer
from taggit_serializer.serializers import TaggitSerializer

from ..models import Post


class PostSerializer(TaggitSerializer, ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
