import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whatyouknow.settings")
django.setup()

if __name__ == '__main__':
    from fixtures import make_objects
    make_objects(factor=100, create_superuser=False)