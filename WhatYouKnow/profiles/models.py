from django.db import models
from django.contrib.auth.models import AbstractUser

# from easy_thumbnails.fields import ThumbnailerImageField


class ProfileUser(AbstractUser):
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    # , height_field=100, width_field=100)
    # image = ThumbnailerImageField(upload_to='profile_images', null=True, blank=True)
    name = models.CharField(max_length=254, blank=False)
    # type = models.CharField(max_length=1, choices={(1, 'Инструктор'), (2, 'Тренер'), (3, 'Персонал')})
    # email = models.EmailField(_('email address'), blank=True)
    website = models.URLField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_image_url(self):
        if self.image:
            return getattr(self.image, "url", None)
        return None
