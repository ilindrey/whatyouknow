from rest_framework.serializers import ModelSerializer, CreateOnlyDefault
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from apps.core.api.fields import IsNullSetDefaultJSONField
from ..models import Profile, default_settings


class ProfileSerializer(TaggitSerializer, ModelSerializer):
    excluded_feed_tags = TagListSerializerField()
    settings = IsNullSetDefaultJSONField(initial=default_settings,
                                         default=CreateOnlyDefault(default_settings))

    class Meta:
        model = Profile
        exclude = ('email', 'password')
        read_only_fields = ('is_active', 'is_staff', 'user_permissions', 'groups')
        extra_kwargs = {
            'email':
                {'write_only': True},

            'password':
                {'write_only': True}
            }

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class CreateProfileSerializer(ProfileSerializer):

    class Meta(ProfileSerializer.Meta):
        fields = ('username', 'email', 'password')
        exclude = None
