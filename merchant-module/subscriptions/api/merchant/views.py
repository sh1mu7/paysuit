from rest_framework import viewsets, mixins

from subscriptions.models import Package, Subscription
from . import serializers


class MerchantPackageAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Package.objects.filter(is_active=True)
    serializer_class = serializers.MerchantPackageListSerializer


class MerchantSubscribeAPI(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Subscription.objects.all()
    serializer_class = serializers.MerchantSubscribeSerializer


class MerchantSubscriptionHistoryAPI(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Subscription.objects.all()
    serializer_class = serializers.MerchantSubscriptionListSerializer

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
