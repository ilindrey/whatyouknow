
def main(*args, **kwargs):
    import os
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
    django.setup()

    from .fixtures import make_objects
    factor = (args[0] if len(args) > 0 else kwargs.get('factor')) or 5
    make_objects(factor)
