from .factories import PostFactory

from whatyouknow.blog.models import Post
from whatyouknow.profiles.models import UserProfile


def make_objects(post_count=100):

    Post.objects.all().delete()
    UserProfile.objects.filter(is_superuser=False).delete()

    PostFactory.create_batch(size=post_count)
