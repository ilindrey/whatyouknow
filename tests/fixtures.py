from reference import ReferenceModel as rm

from factories import SuperUserFactory, UserProfileFactory, PostFactory, PostCommentsFactory


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

    user_count = 20
    post_count = 10

    post_comments_factor = 100

    total_count = user_count * factor
    UserProfileFactory.create_batch(size=total_count)
    print_create_batch_info(UserProfileFactory, total_count)

    total_count = post_count * factor
    PostFactory.create_batch(size=total_count)
    print_create_batch_info(PostFactory, total_count)

    total_count = post_count * post_comments_factor * factor
    PostCommentsFactory.create_batch(size=total_count)
    print_create_batch_info(PostCommentsFactory, total_count)


def print_cleared_model(model, extra_msg=None):
    msg = model.__name__ + ' model was cleared.'
    if extra_msg:
        msg += ' ' + extra_msg
    print(msg)


def print_create_batch_info(factory, count):
    print('Factory ' + factory.__name__ + ' created batch ' + str(count) + ' count.')
