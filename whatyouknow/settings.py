"""
Django settings for whatyouknow project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # default django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'django.forms',

    # other django apps
    # 'django.contrib.sites',

    # other apps
    'django_summernote',
    'taggit',
    'mptt',
    'versatileimagefield',

    # setting apps
    'whatyouknow.summernote',

    # project apps
    'whatyouknow.core',
    'whatyouknow.profiles',
    'whatyouknow.blog',
    'whatyouknow.comments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'whatyouknow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'whatyouknow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'profiles.Profile'

LOGIN_REDIRECT_URL = 'index'

# FORM_RENDERER = 'django.forms.renderers.DjangoTemplates'

# django-summernote
X_FRAME_OPTIONS = 'SAMEORIGIN'

SUMMERNOTE_CONFIG = {
    'summernote': {
        # 'width': 1366,
        # 'height': 720,
        # 'fontNames': ['Arial'],
        # 'fontNamesIgnoreCheck': ['Open Sans'],
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript',
                      'strikethrough', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['list', ['ul', 'ol']],
            ['para', ['paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video', 'hr']],
            ['view', ['fullscreen', 'codeview']],
            ['help', ['help']],
            ],
        'popover': {
            'image': [
                ['custom', ['imageAttributes']],
                ['imagesize', ['imageSize100', 'imageSize50', 'imageSize25']],
                ['float', ['floatLeft', 'floatRight', 'floatNone']],
                ['remove', ['removeMedia']],
                ],
            },
        'imageAttributes': {
            'icon': '<i class="note-icon-pencil"/>',
            'figureClass': '',
            'figcaptionClass': '',
            'captionText': 'Caption Goes Here.',
            'manageAspectRatio': True  # true = Lock the Image Width/Height, Default to true
            },
        },
    'js': (
        '/static/summernote/plugins/summernote-image-attribute-editor/summernote-image-attributes.js',
        '/static/summernote/plugins/summernote-image-attribute-editor/lang/en-us.js',
        ),
    'css': (
        '/static/core/css/fonts.css',
        ),
    'js_for_inplace': (
        '/static/summernote/plugins/summernote-image-attribute-editor/summernote-image-attributes.js',
        '/static/summernote/plugins/summernote-image-attribute-editor/lang/en-us.js',
        ),
    'css_for_inplace': (
        '/static/core/css/fonts.css',
        ),
    }


# django-versatileimagefield

VERSATILEIMAGEFIELD_SETTINGS = {
    # The amount of time, in seconds, that references to created images
    # should be stored in the cache. Defaults to `2592000` (30 days)
    'cache_length': 2592000,
    # The name of the cache you'd like `django-versatileimagefield` to use.
    # Defaults to 'versatileimagefield_cache'. If no cache exists with the name
    # provided, the 'default' cache will be used instead.
    'cache_name': 'versatileimagefield_cache',
    # The save quality of modified JPEG images. More info here:
    # https://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html#jpeg
    # Defaults to 70
    'jpeg_resize_quality': 100,
    # The name of the top-level folder within storage classes to save all
    # sized images. Defaults to '__sized__'
    'sized_directory_name': '__sized__',
    # The name of the directory to save all filtered images within.
    # Defaults to '__filtered__':
    'filtered_directory_name': '__filtered__',
    # The name of the directory to save placeholder images within.
    # Defaults to '__placeholder__':
    'placeholder_directory_name': '__placeholder__',
    # Whether or not to create new images on-the-fly. Set this to `False` for
    # speedy performance but don't forget to 'pre-warm' to ensure they're
    # created and available at the appropriate URL.
    'create_images_on_demand': False,
    # A dot-notated python path string to a function that processes sized
    # image keys. Typically used to md5-ify the 'image key' portion of the
    # filename, giving each a uniform length.
    # `django-versatileimagefield` ships with two post processors:
    # 1. 'versatileimagefield.processors.md5' Returns a full length (32 char)
    #    md5 hash of `image_key`.
    # 2. 'versatileimagefield.processors.md5_16' Returns the first 16 chars
    #    of the 32 character md5 hash of `image_key`.
    # By default, image_keys are unprocessed. To write your own processor,
    # just define a function (that can be imported from your project's
    # python path) that takes a single argument, `image_key` and returns
    # a string.
    'image_key_post_processor': None,
    # Whether to create progressive JPEGs. Read more about progressive JPEGs
    # here: https://optimus.io/support/progressive-jpeg/
    'progressive_jpeg': False
}

VERSATILEIMAGEFIELD_USE_PLACEHOLDIT = False


VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'profile_avatar': [
        ('full_size', 'url'),
        ('avatar_crop', 'crop__28x28'),
        ('comment_avatar_crop', 'crop__35x35'),
        # ('mini_crop', 'crop__35x35'),
        # ('tiny_crop', 'crop__80x80'),
        # ('small_crop', 'crop__150x150'),
        ('medium_crop', 'crop__300x300'),
        # ('large_crop', 'crop__450x450'),
        # ('big_crop', 'crop__600x600'),
        # ('huge_crop', 'crop__800x800'),
        # ('massive_crop', 'crop__960x960'),
    ],
    'post_feed_cover': [
        ('full_size', 'url'),
        ('feed_cover_crop', 'crop__360x250'),
    ],
}