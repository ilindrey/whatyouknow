from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from taggit.managers import TaggableManager

from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from versatileimagefield.placeholder import OnStoragePlaceholderImage

from whatyouknow.storages import AssetsStorage


UPLOAD_TO_AVATAR = 'profiles/avatars/'


class Profile(AbstractUser):
    avatar = VersatileImageField(
        _('avatar'),
        upload_to=UPLOAD_TO_AVATAR,
        blank=True,
        ppoi_field='avatar_ppoi',
        placeholder_image=OnStoragePlaceholderImage(
            path=UPLOAD_TO_AVATAR + 'avatar_placeholder.png',
            storage=AssetsStorage())
        )
    avatar_ppoi = PPOIField()
    name = models.CharField(_('name'), max_length=300, blank=False)
    first_name = None  # abstract model field, removed
    last_name = None  # abstract model field, removed
    email = models.EmailField(_('email address'),   # abstract blank is True, unique is not specified
                              unique=True,
                              blank=False)
    specialization = models.CharField(_('specialization'), max_length=100, blank=True)
    description = models.TextField(_('description'), max_length=1000, blank=True)
    tags = TaggableManager()
    settings = models.JSONField(_('settings'), default=dict, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username']

    def __str__(self):
        return self.name + ' @' + self.username

    @property
    def get_avatar_url(self):
        if self.avatar:
            return getattr(self.avatar, "url", None)
        return None


@receiver(models.signals.post_save, sender=Profile)
def warm_Profile_avatar_images(sender, instance, **kwargs):
    """Ensures Person head shots are created post-save"""
    profile_img_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='profile_avatar',
        image_attr='avatar'
    )
    num_created, failed_to_create = profile_img_warmer.warm()
    # profile_img_warmer.warm()
