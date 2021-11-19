from django.urls import path, include
from rest_framework.authtoken import views

from apps.profiles.api.urls import router as profiles_router
from apps.blog.api.urls import router as blog_router
from apps.comments.api.urls import router as comments_router

from .routers import DefaultRouter


router = DefaultRouter()
router.extend(profiles_router)
router.extend(blog_router)
router.extend(comments_router)


urlpatterns = [
    path('',            include(router.urls)),
    path('auth/',       include('rest_framework.urls')),
    path('auth/token/', views.obtain_auth_token),
]