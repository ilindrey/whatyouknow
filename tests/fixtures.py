from .reference import ReferenceModel as rm

from .factories import SuperUserFactory, UserProfileFactory, PostFactory, PostCommentsFactory


def make_objects(factor=1, create_superuser=False):

    rm.COMMENT.objects.all().delete()
    rm.POST.objects.all().delete()

    if create_superuser:
        rm.USER.objects.all().delete()
        SuperUserFactory.create()
    else:
        rm.USER.objects.filter(is_superuser=False).delete()

    UserProfileFactory.create_batch(size=20*factor)
    PostFactory.create_batch(size=10*factor)
    PostCommentsFactory.create_batch(100*factor)
