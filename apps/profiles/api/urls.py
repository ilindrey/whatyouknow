from rest_framework.routers import DefaultRouter

from .views import CreateProfileAPIViewSet, RetrieveUpdateDestroyListProfileAPIViewSet

router = DefaultRouter()
router.register('profiles/create/', CreateProfileAPIViewSet)
router.register('profiles', RetrieveUpdateDestroyListProfileAPIViewSet)
