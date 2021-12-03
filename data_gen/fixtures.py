
from random import randint
from shutil import rmtree

from concurrent.futures import ThreadPoolExecutor

from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from easy_thumbnails.models import Source, Thumbnail, ThumbnailDimensions
from taggit.models import Tag, TaggedItem
from django_summernote.models import Attachment

from apps.blog.models import Post
from apps.comments.models import Comment

from .factories import StaffGroupFactory, SuperUserFactory, CommonProfileFactory, StaffProfileFactory, PostFactory, PostCommentsFactory


USER_MODEL = get_user_model()


def make_objects(factor):

    staff_user_count = factor
    common_user_count = staff_user_count * randint(5, 10)
    post_count = common_user_count * randint(5, 10)
    post_comments_count = post_count * randint(75, 125)

    factories = {
        SuperUserFactory: 1,
        StaffGroupFactory: 1,
        StaffProfileFactory: staff_user_count,
        CommonProfileFactory: common_user_count,
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
    run_cleanup_model(Attachment)

    cleanup_media_files()  # delete all media files

    print_divider()

    for factory, count in factories.items():
        if count > 1:
            run_create_batch(factory, count)
        else:
            run_create(factory)

    print_divider()

    print('Data generation completed.')


def print_divider():
    print('====================================================================')


def print_info_total(factories):
    print('Total will created by factories:')
    for factory, count in factories.items():
        print(f'{factory.__name__} --> {count}')


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
        print("The MEDIA_ROOT directory was cleared.")
    except OSError as e:
        print(f'Error: {e.strerror}')


def run_cleanup_model(model, extra_msg=None):
    model.objects.all().delete()
    msg = f'{model.__name__} model was cleared.'
    if extra_msg:
        msg += str(extra_msg)
    print(msg)


def run_create(factory):
    print(f'Start creating of the {factory.__name__} factory.')
    factory.create()
    print(f'+++++ Factory {factory.__name__} was created. +++++')


def run_create_batch(factory, size):
    print(f'Start creating {size} records of the {factory.__name__} factory.')
    with ThreadPoolExecutor() as executor:
        for _ in range(size):
            executor.submit(factory.create)
    print(f'+++++ Factory {factory.__name__} created batch {size} count. +++++')
