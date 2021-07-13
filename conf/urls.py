"""whatyouknow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the includes() function: from django.urls import includes, path
    2. Add a URL to urlpatterns:  path('blog/', includes('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


api_patterns = [
    path('', include('apps.profiles.api.urls')),
]

urlpatterns = [
    # apps
    path('', include('apps.core.urls')),
    path('profiles/', include('apps.profiles.urls')),
    path('posts/', include('apps.blog.urls')),
    path('comments/', include('apps.comments.urls')),
    # default apps
    path('admin/', admin.site.urls),
    # others
    path('summernote/', include('django_summernote.urls')),
    # api
    path('api/', include(api_patterns)),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
