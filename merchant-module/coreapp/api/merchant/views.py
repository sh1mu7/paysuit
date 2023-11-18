from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser
from . import serializers
from ...models import BusinessDocument, Business


class MerchantBusinessAPI(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.MerchantBusinessCreateSerializer
    queryset = Business.objects.all()


class MerchantBusinessDocumentAPI(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.MerchantLegalDocumentUploadSerializer
    queryset = BusinessDocument.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
