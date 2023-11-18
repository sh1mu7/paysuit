from rest_framework import serializers

from subscriptions.models import Package


class PackageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'
