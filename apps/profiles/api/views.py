from rest_framework.permissions import AllowAny

from ..models import Profile
from .viewsets import CreateModelViewSet, RetrieveUpdateDestroyListModelViewSet
from .serializers import CreateProfileSerializer, ProfileSerializer


class CreateProfileAPIViewSet(CreateModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = CreateProfileSerializer
    permission_classes = [AllowAny]


class RetrieveUpdateDestroyListProfileAPIViewSet(RetrieveUpdateDestroyListModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
