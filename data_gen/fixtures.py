
from random import randint
from shutil import rmtree

from concurrent.futures import ThreadPoolExecutor

from django.core.files.storage import default_storage

from factory.django import get_model

from .factories import StaffGroupFactory, SuperUserFactory, CommonProfileFactory, StaffProfileFactory, PostFactory, PostCommentsFactory


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

    cleaning_list = [
        'comments.comment',
        'blog.post',
        'auth.Group',
        'profiles.Profile',
        'easy_thumbnails.ThumbnailDimensions',
        'easy_thumbnails.Thumbnail',
        'easy_thumbnails.Source',
        'taggit.TaggedItem',
        'taggit.Tag',
        'django_summernote.Attachment'
    ]
    run_cleanup_models(cleaning_list)
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


def get_model_class(definition):
    # code based on https://github.com/FactoryBoy/factory_boy/blob/371815b219d0f91c3032fdd479fc2ef7d1d3af6b/factory/django.py#L90
    if isinstance(definition, str) and '.' in definition:
        app, model = definition.split('.', 1)
        return get_model(app, model)

    return definition


def run_cleanup_models(model_list=[]):
    for model in model_list:
        run_cleanup_model(model)


def run_cleanup_model(definition, extra_msg=None):
    model = get_model_class(definition)
    model.objects.all().delete()
    msg = f'{model.__name__} model was cleared.'
    if extra_msg:
        msg += str(extra_msg)
    print(msg)


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
