from rest_framework.routers import DefaultRouter

from .views import PostAPIViewSet


router = DefaultRouter()
router.register('posts', PostAPIViewSet)
