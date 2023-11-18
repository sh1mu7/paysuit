from rest_framework import serializers

from subscriptions.models import Package, Subscription


class MerchantPackageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'name', 'registration_fee', 'renewal_fee', 'local', 'international', 'mfs', 'desc')


class MerchantSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'business', 'amount', 'expiry_date')


class MerchantSubscriptionListSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(source='get_is_active')

    class Meta:
        model = Subscription
        fields = ('id', 'business', 'amount', 'expiry_date', 'is_active')
