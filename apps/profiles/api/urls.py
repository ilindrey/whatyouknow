from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import CreateProfileAPIViewSet, RetrieveUpdateDestroyListProfileAPIViewSet

router = DefaultRouter()
router.register('profiles/create/', CreateProfileAPIViewSet)
router.register('profiles', RetrieveUpdateDestroyListProfileAPIViewSet)


urlpatterns = [
    path('',            include(router.urls)),
    path('auth/',       include('rest_framework.urls')),
    path('auth/token/', views.obtain_auth_token),
]