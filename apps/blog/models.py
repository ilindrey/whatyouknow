from enum import Flag
from random import choice as random_choice

from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from django_summernote.fields import SummernoteTextField
from taggit.managers import TaggableManager
from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from versatileimagefield.placeholder import OnStoragePlaceholderImage

# from whatyouknow.storages import AssetsStorage


# UPLOAD_TO_FEED_CODER = 'blog/feed_covers'


class CategoryTypes(Flag):
    DEVELOPMENT = (0, "Development")
    ADMINISTRATING = (1, "Administrating")
    DESIGN = (2, "Design")
    MANAGEMENT = (3, "Management")
    MARKETING = (4, "Marketing")
    POPULAR_SCIENCE = (5, "Popular Science")

    @classmethod
    def choices(cls):
        return [key.value for key in cls]

    @classmethod
    def get_random(cls):
        return random_choice(cls.choices())

    @classmethod
    def get_random_index(cls):
        return cls.get_random()[0]

    @classmethod
    def get_name(cls, index):
        return cls.choices()[index][1]


class Post(models.Model):

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT
        )
    publish = models.DateTimeField(default=timezone.now)
    category = models.IntegerField(choices=CategoryTypes.choices())
    title = models.CharField(max_length=200)
    text = SummernoteTextField()
    feed_cover = VersatileImageField(
        'feed_cover',
        upload_to='blog/feed_covers',
        blank=False,
        ppoi_field='feed_cover_ppoi',
        )
    feed_cover_ppoi = PPOIField()
    feed_article_preview = SummernoteTextField(null=True, blank=True)
    tags = TaggableManager()

    class Meta:
        verbose_name_plural = 'Posts'
        ordering = ('-publish', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


@receiver(models.signals.post_save, sender=Post)
def warm_Profile_avatar_images(sender, instance, **kwargs):
    """Ensures Person head shots are created post-save"""
    post_img_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='post_feed_cover',
        image_attr='feed_cover'
    )
    num_created, failed_to_create = post_img_warmer.warm()
