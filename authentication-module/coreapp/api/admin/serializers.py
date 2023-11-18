from rest_framework import serializers

from ...models import Country, Module, ModulePermission, PermissionGroup, UserPermission, LoginHistory


class CountryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class ModuleAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class ModulePermissionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModulePermission
        fields = '__all__'


class PermissionGroupAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionGroup
        fields = '__all__'

    def create(self, validated_data):
        permissions = validated_data.pop('permissions')
        instance = self.Meta.model.objects.create(**validated_data)
        instance.permissions.set(permissions)
        instance.save()
        instance.refresh_from_db()
        return instance

    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions')
        self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
        instance.permissions.set(permissions)
        instance.refresh_from_db()
        return instance


class UserPermissionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = '__all__'


class UserLoginHistoryAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = '__all__'
