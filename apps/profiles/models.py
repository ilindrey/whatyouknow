from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global
from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from taggit.managers import TaggableManager


def default_settings():
    from apps.blog.models import CategoryTypes
    return {'feed_categories': CategoryTypes.list('index')}


class Profile(AbstractUser):
    avatar = models.ImageField(
        _('avatar'),
        upload_to='profiles/avatars/',
        blank=True)
    name = models.CharField(_('name'), max_length=300, blank=True)
    first_name = None  # abstract model field, removed
    last_name = None  # abstract model field, removed
    email = models.EmailField(_('email address'),   # abstract blank is True, unique is not specified
                              unique=True,
                              blank=False)
    specialization = models.CharField(_('specialization'), max_length=100, blank=True)
    description = models.TextField(_('description'), max_length=1000, blank=True)
    excluded_feed_tags = TaggableManager()
    settings = models.JSONField(_('settings'), default=default_settings, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

    def __str__(self):
        return self.username

    def get_avatar(self, size):
        if self.avatar:
            return thumbnail_url(self.avatar, size)
        else:
            return static('profiles/image/avatar_placeholder.svg')


@receiver(post_save, sender=Profile)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


saved_file.connect(generate_aliases_global)

