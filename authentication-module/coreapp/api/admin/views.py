from django_filters import rest_framework as dj_filters
from rest_framework import viewsets, permissions, generics
from . import serializers
from .. import filters
from ...models import Country, Module, ModulePermission, PermissionGroup, UserPermission, LoginHistory


class CountryAdminAPI(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser, ]
    queryset = Country.objects.all()
    serializer_class = serializers.CountryAdminSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.CountryFilter


class ModuleAdminAPI(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser, ]
    queryset = Module.objects.all()
    serializer_class = serializers.ModuleAdminSerializer


class ModulePermissionAdminAPI(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser, ]
    queryset = ModulePermission.objects.all()
    serializer_class = serializers.ModulePermissionAdminSerializer


class PermissionGroupAdminAPI(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser, ]
    queryset = PermissionGroup.objects.all()
    serializer_class = serializers.PermissionGroupAdminSerializer


class UserPermissionAdminAPI(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser, ]
    queryset = UserPermission.objects.all()
    serializer_class = serializers.UserPermissionAdminSerializer


class LoginHistoryAdminAPI(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser, ]
    queryset = LoginHistory.objects.all()
    serializer_class = serializers.UserLoginHistoryAdminSerializer
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.LoginHistoryFilter
