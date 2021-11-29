
def js_bool_format(value):
    return str(value).lower()


def has_permssions(user, obj, perm_list=['change', 'view']):
    if hasattr(obj, '_meta') and hasattr(obj._meta, 'app_label') and hasattr(obj._meta, 'model_name'):
        return user.has_perms(f'{obj._meta.app_label}.{perm}_{obj._meta.model_name}' for perm in perm_list)
    return False


def author_or_has_permssions(user, obj, perm_list=['change', 'view']):
    has_perms = has_permssions(user, obj, perm_list)
    return hasattr(obj, 'user') and obj.user == user or has_perms
