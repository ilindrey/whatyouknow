from random import randint
from shutil import rmtree

from django.core.files.storage import default_storage

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

    # user_count = randint(1, factor)
    # post_count = randint(factor, user_count * factor)
    #
    # post_comments_factor = randint(post_count, post_count * factor)

    user_count = 1
    post_count = 100

    post_comments_factor = 10

    SuperUserFactory.create()
    print('Superuser was created.')

    total_count = user_count * factor
    print_start_create_info(ProfileFactory, total_count)
    ProfileFactory.create_batch(size=total_count)
    print_create_batch_info(ProfileFactory, total_count)

    total_count = post_count * factor
    print_start_create_info(PostFactory, total_count)
    PostFactory.create_batch(size=total_count)
    print_create_batch_info(PostFactory, total_count)

    total_count = post_count * post_comments_factor * factor
    print_start_create_info(PostCommentsFactory, total_count)
    PostCommentsFactory.create_batch(size=total_count)
    print_create_batch_info(PostCommentsFactory, total_count)


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


def print_start_create_info(factory, count):
    print('Start creating ' + str(count) + ' records of the ' + factory.__name__ + ' factory.')


def print_create_batch_info(factory, count):
    print('-- Factory ' + factory.__name__ + ' created batch ' + str(count) + ' count.')
