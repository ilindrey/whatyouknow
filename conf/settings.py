"""
Django settings for whatyouknow project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path  # Django >=3.0
# import os  # Django 2.2/

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
    # 'django.contrib.sites',
    # packages
    'mptt',
    'taggit',
    'easy_thumbnails',
    'django_summernote',
    # packages customization apps
    'apps_packages.summernote',
    # project apps
    'apps.core',
    'apps.profiles',
    'apps.blog',
    'apps.comments',
    # rest API
    'rest_framework',
    'rest_framework.authtoken',
    'taggit_serializer',
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

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # Django >=3.0
        # 'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Django 2.2
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

WSGI_APPLICATION = 'conf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Django >=3.0
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # Django 2.2
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

# Django >=3.0
STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/{}/'.format(STATIC_ROOT.name)

# Django 2.2
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_URL = '/static/'


# Media files

# Django >=3.0
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/{}/'.format(MEDIA_ROOT.name)

# Django 2.2
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'


# User model

AUTH_USER_MODEL = 'profiles.Profile'


# login

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'

# sessions

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# django.contrib.sites

# SITE_ID = 1

# caches

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': 'default'
#         }
#     }

# email

EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)

# django-summernote

SUMMERNOTE_THEME = 'bs3'
X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': 672,
        # 'height': 720,
        # 'fontNames': ['Arial'],
        # 'fontNamesIgnoreCheck': ['Open Sans'],
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript',
                      'strikethrough', 'clear']],
            # ['fontname', ['fontname']],
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


# easy_thumbnails

THUMBNAIL_DEFAULT_OPTIONS = {
    'quality': 100, 'subsampling': 2
    }

THUMBNAIL_ALIASES = {
    'profiles.Profile.avatar': {
        'default':
            {
                'size': (28, 28),
                'crop': 'smart',
                },
        'comment':
            {
                'size': (35, 35),
                'crop': 'smart',
                },
        'tiny': {
            'size': (80, 80),
            'crop': 'smart',
            },
        'small':  # semantic image size
            {
                'size': (150, 150),
                'crop': 'smart',
                }
        },
    'blog.Post.feed_cover': {
        'default':
            {
                'size': (360, 250),
                'crop': 'smart',

                },
        'item':
            {
                'size': (180, 125),
                'crop': 'smart',
                },
        }
    }


# rest_framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
        ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 15
    }
