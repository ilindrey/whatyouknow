from django.conf import settings
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

    user_count = 1
    post_count = 50

    post_comments_factor = 100

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

    avatar_upload_to = rm.USER.avatar.field.upload_to
    feed_cover_upload_to = rm.POST.feed_cover.field.upload_to
    sized_directory_name = settings.VERSATILEIMAGEFIELD_SETTINGS['sized_directory_name']
    filtered_directory_name = settings.VERSATILEIMAGEFIELD_SETTINGS['filtered_directory_name']
    placeholder_directory_name = settings.VERSATILEIMAGEFIELD_SETTINGS['placeholder_directory_name']

    path_avatar = location / avatar_upload_to
    path_feed_cover = location / feed_cover_upload_to
    path_sized = location / sized_directory_name
    path_filtered = location / filtered_directory_name
    path_placeholder = location / placeholder_directory_name

    remove_files_dir(path_avatar)
    remove_files_dir(path_feed_cover)

    descendant_list = [
        avatar_upload_to,
        feed_cover_upload_to
        ]

    remove_files_versatile_dir(path_sized, descendant_list)
    remove_files_versatile_dir(path_filtered, descendant_list)
    remove_files_versatile_dir(path_placeholder, descendant_list)


def remove_files_dir(path):
    if not path.exists():
        return

    try:
        files = path.glob('*.*')
        for file in files:
            file.unlink()
    except OSError as e:
        print("Error: %s : %s" % (path, e.strerror))


def remove_files_versatile_dir(path, descendant_list):
    for descendant in descendant_list:
        remove_files_dir(path / descendant)


def print_cleared_model(model, extra_msg=None):
    msg = model.__name__ + ' model was cleared.'
    if extra_msg:
        msg += ' ' + extra_msg
    print(msg)


def print_start_create_info(factory, count):
    print(factory.__name__ + ' factory of ' + str(count) + ' records is currently being created.')


def print_create_batch_info(factory, count):
    print('Factory ' + factory.__name__ + ' created batch ' + str(count) + ' count.')
