from django_filters import rest_framework as dj_filters
from rest_framework import viewsets, permissions, generics, mixins
from rest_framework.permissions import IsAdminUser

from . import serializers
from .. import filters
from ...models import Business, BusinessCategory, BusinessDocument


class AdminBusinessCategoryAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = BusinessCategory.objects.all()
    serializer_class = serializers.AdminBusinessCategorySerializer

    def get_serializer_class(self):
        if self.action == 'create' or 'update':
            return serializers.AdminBusinessCreateSerializer
        return self.serializer_class


class AdminBusinessAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.AdminBusinessListSerializer
    queryset = Business.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or 'update':
            return serializers.AdminBusinessCreateSerializer
        return self.serializer_class


class AdminBusinessDocumentAPI(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.AdminBusinessDocumentListSerializer
    queryset = BusinessDocument.objects.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return serializers.AdminBusinessDocumentConfirmationSerializer
        return self.serializer_class
