from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, \
    UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet


class CreateModelViewSet(CreateModelMixin, GenericViewSet):
    pass


class RetrieveUpdateDestroyListModelViewSet(RetrieveModelMixin,
                                            UpdateModelMixin,
                                            DestroyModelMixin,
                                            ListModelMixin,
                                            GenericViewSet):
    pass
