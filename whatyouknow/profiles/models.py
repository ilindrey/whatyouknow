from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _

# from easy_thumbnails.fields import ThumbnailerImageField


class UserProfile(AbstractUser):
    image = models.ImageField(upload_to="profiles/", null=True, blank=True)
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(_('email address'),   # abstract blank is True, unique is not specified
                              unique=True,
                              blank=False)
    specialization = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)  # delete
    description = models.TextField(max_length=1000, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.name

    @property
    def get_image_url(self):
        if self.image:
            return getattr(self.image, "url", None)
        return None
