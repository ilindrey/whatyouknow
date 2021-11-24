from random import randint
from shutil import rmtree

from django.core.files.storage import default_storage

from easy_thumbnails.models import Source, Thumbnail, ThumbnailDimensions
from taggit.models import Tag, TaggedItem

from .reference import ReferenceModel as rm
from .factories import SuperUserFactory, ProfileFactory, PostFactory, PostCommentsFactory


def make_objects(factor=1):

    rm.COMMENT.objects.all().delete()
    print_cleared_model(rm.COMMENT)

    rm.POST.objects.all().delete()
    print_cleared_model(rm.POST)

    rm.USER.objects.all().delete()
    print_cleared_model(rm.USER)

    clear_media_files()  # delete all media files

    ThumbnailDimensions.objects.all().delete()
    Thumbnail.objects.all().delete()
    Source.objects.all().delete()

    TaggedItem.objects.all().delete()
    Tag.objects.all().delete()

    user_count = randint(1, factor)
    post_count = randint(factor, user_count * factor)

    post_comments_factor = randint(post_count, post_count * factor)

    SuperUserFactory.create()
    print('Superuser was created.')

    run_create_batch(ProfileFactory, user_count * factor)
    run_create_batch(PostFactory, post_count * factor)
    run_create_batch(PostCommentsFactory, post_count * post_comments_factor * factor)


def run_create_batch(factory, size):
    print_info_create_start(factory, size)
    factory.create_batch(size=size)
    print_info_create_complete(factory, size)


def clear_media_files():
    """
        Delete MEDIA_ROOT directory with media files
    :return:
    """
    location = default_storage.base_location
    try:
        listdir = default_storage.listdir(location)[0]
        for dir in listdir:
            rmtree(default_storage.path(dir))
    except OSError as e:
        print("Error: %s" % e.strerror)


def print_cleared_model(model, extra_msg=None):
    msg = model.__name__ + ' model was cleared.'
    if extra_msg:
        msg += ' ' + extra_msg
    print(msg)


def print_info_create_start(factory, count):
    print('Start creating ' + str(count) + ' records of the ' + factory.__name__ + ' factory.')


def print_info_create_complete(factory, count):
    print('-- Factory ' + factory.__name__ + ' created batch ' + str(count) + ' count.')
