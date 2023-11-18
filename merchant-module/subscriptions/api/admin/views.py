from rest_framework import viewsets
from django_filters import rest_framework as dj_filters
from rest_framework.permissions import IsAdminUser

from . import serializers
from .. import filters
from ...models import Package


class PackageAdminAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Package.objects.all()
    serializer_class = serializers.PackageAdminSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.PackageFilter
