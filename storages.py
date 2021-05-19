from django.conf import settings
from django.core.files.storage import FileSystemStorage


class AssetsStorage(FileSystemStorage):
    location = settings.BASE_DIR / 'assets/'
