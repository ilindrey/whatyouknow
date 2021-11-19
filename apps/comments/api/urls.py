from rest_framework.routers import DefaultRouter

from .views import CommentAPIViewSet


router = DefaultRouter()
router.register('comments', CommentAPIViewSet)
