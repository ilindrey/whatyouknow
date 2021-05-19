import shutil
from shutil import rmtree

from django.conf import settings
from django.core.files.storage import default_storage

from .reference import ReferenceModel as rm
from .factories import SuperUserFactory, ProfileFactory, PostFactory, PostCommentsFactory


def make_objects(factor=1, create_superuser=False):

    rm.COMMENT.objects.all().delete()
    print_cleared_model(rm.COMMENT)
    rm.POST.objects.all().delete()
    print_cleared_model(rm.POST)

    if create_superuser:
        rm.USER.objects.all().delete()
        print_cleared_model(rm.USER)
    else:
        rm.USER.objects.filter(is_superuser=False).delete()
        print_cleared_model(rm.USER, 'Superuser was not deleted.')

    clear_media_files(create_superuser)  # delete all media files

    user_count = 1
    post_count = 50

    post_comments_factor = 100

    if create_superuser:
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


def print_cleared_model(model, extra_msg=None):
    msg = model.__name__ + ' model was cleared.'
    if extra_msg:
        msg += ' ' + extra_msg
    print(msg)


def print_start_create_info(factory, count):
    print(factory.__name__ + ' factory of ' + str(count) + ' records is currently being created.')


def print_create_batch_info(factory, count):
    print('Factory ' + factory.__name__ + ' created batch ' + str(count) + ' count.')


def clear_media_files(create_superuser):
    """
        Delete MEDIA_ROOT directory with media files
    :return:
    """
    location = default_storage.base_location
    sua_filename = SuperUserFactory.avatar._defaults['filename']

    path_avatar = location / rm.USER.avatar.field.upload_to
    path_feed_cover = location / rm.POST.feed_cover.field.upload_to
    path_sized = location / settings.VERSATILEIMAGEFIELD_SETTINGS['sized_directory_name']
    path_filtered = location / settings.VERSATILEIMAGEFIELD_SETTINGS['filtered_directory_name']
    path_placeholder = location / settings.VERSATILEIMAGEFIELD_SETTINGS['placeholder_directory_name']

    if not create_superuser:
        path_sua_original = path_avatar / sua_filename
        path_sua_copy = location / sua_filename
        shutil.copyfile(path_sua_original, path_sua_copy)

    remove_files_dir(path_avatar)
    remove_files_dir(path_feed_cover)
    remove_files_dir(path_sized)
    remove_files_dir(path_filtered)
    remove_files_dir(path_placeholder)

    if not create_superuser:
        shutil.copyfile(path_sua_copy, path_sua_original)
        path_sua_copy.unlink()


def remove_files_dir(path):
    if not path.exists():
        return

    try:
        files = path.glob('*.*')
        for file in files:
            file.unlink()
    except OSError as e:
        print("Error: %s : %s" % (path, e.strerror))
