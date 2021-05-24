
def main():
    import os
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
    django.setup()

    from .fixtures import make_objects
    make_objects(factor=10)
