from reference import ReferenceModel as rm

from factories import SuperUserFactory, ProfileFactory, PostFactory, PostCommentsFactory


def make_objects(factor=1, create_superuser=False):

    rm.COMMENT.objects.all().delete()
    print_cleared_model(rm.COMMENT)
    rm.POST.objects.all().delete()
    print_cleared_model(rm.POST)

    if create_superuser:
        rm.USER.objects.all().delete()
        print_cleared_model(rm.USER)

        SuperUserFactory.create()
        print('Superuser was created.')
    else:
        rm.USER.objects.filter(is_superuser=False).delete()
        print_cleared_model(rm.USER, 'Superuser was not deleted.')

    user_count = 1
    post_count = 50

    post_comments_factor = 100

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
