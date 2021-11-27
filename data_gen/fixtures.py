
from random import randint
from shutil import rmtree

from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from easy_thumbnails.models import Source, Thumbnail, ThumbnailDimensions
from taggit.models import Tag, TaggedItem

from apps.blog.models import Post
from apps.comments.models import Comment

from .factories import StaffGroupFactory, SuperUserFactory, ProfileFactory, PostFactory, PostCommentsFactory


USER_MODEL = get_user_model()


def make_objects(factor):

    user_count = round(randint(factor, factor**2) / factor) * factor
    post_count = user_count * randint(5, 10)
    post_comments_count = post_count * randint(75, 125)

    factories = {
        SuperUserFactory: 1,
        StaffGroupFactory: 1,
        ProfileFactory: user_count,
        PostFactory: post_count,
        PostCommentsFactory: post_comments_count,
    }

    print(f'Start generating data with a factor - {factor}.')

    print_info_total(factories)

    print_divider()

    run_cleanup_model(Comment)
    run_cleanup_model(Post)
    run_cleanup_model(Group)
    run_cleanup_model(USER_MODEL)
    run_cleanup_model(ThumbnailDimensions)
    run_cleanup_model(Thumbnail)
    run_cleanup_model(Source)
    run_cleanup_model(TaggedItem)
    run_cleanup_model(Tag)

    cleanup_media_files()  # delete all media files

    print_divider()

    for factory, count in factories.items():
        if count > 1:
            run_create_batch(factory, count)
        else:
            run_create(factory)

    print_divider()

    print('Data generation completed.')


def cleanup_media_files():
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
        print(f'Error: {e.strerror}')


def run_cleanup_model(model, **kwargs):
    model.objects.all().delete()
    print_info_cleared_model(model, **kwargs)


def run_create(factory):
    print_info_create_start(factory)
    factory.create()
    print_info_create_complete(factory)


def run_create_batch(factory, size):
    print_info_create_batch_start(factory, size)
    factory.create_batch(size=size)
    print_info_create_batch_complete(factory, size)


def print_divider():
    print('====================================================================')


def print_info_total(factories):
    print('Total will created by factories:')
    for factory, count in factories.items():
        print(f'{factory.__name__} --> {count}')


def print_info_cleared_model(model, extra_msg=None):
    msg = f'{model.__name__} model was cleared.'
    if extra_msg:
        msg += ' ' + extra_msg
    print(msg)


def print_info_create_start(factory):
    print(f'Start creating of the {factory.__name__} factory.')


def print_info_create_complete(factory):
    print(f'+++++ Factory {factory.__name__} was created. +++++')


def print_info_create_batch_start(factory, count):
    print(f'Start creating {count} records of the {factory.__name__} factory.')


def print_info_create_batch_complete(factory, count):
    print(f'+++++ Factory {factory.__name__} created batch {count} count. +++++')
