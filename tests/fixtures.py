from django_comments_xtd.models import XtdComment

from whatyouknow.blog.models import Post
from whatyouknow.profiles.models import UserProfile

from .factories import SuperUserFactory, UserProfileFactory, PostFactory, XtdCommentFactory


def make_objects(factor=1, create_superuser=False):

    XtdComment.objects.all().delete()
    Post.objects.all().delete()

    if create_superuser:
        UserProfile.objects.all().delete()
        SuperUserFactory.create()
    else:
        UserProfile.objects.filter(is_superuser=False).delete()

    UserProfileFactory.create_batch(size=1000*factor)
    PostFactory.create_batch(size=10*factor)
    XtdCommentFactory.create_batch(size=500*factor)
