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

from .settings import DEBUG

from django_js_reverse.views import urls_js

from .blog.views import home, post_detail
# , search_list

urlpatterns = [
    # apps
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('comments/', include('whatyouknow.comments.urls')),
    # others
    path('summernote/', include('django_summernote.urls')),
]


if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
