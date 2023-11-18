from rest_framework import serializers

from coreapp.models import Business, BusinessCategory, BusinessDocument


class AdminBusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = '__all__'


class AdminBusinessListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ('id', 'legal_name', 'address', 'display_name', 'bank_name', 'account_no', 'website', 'status')


class AdminBusinessCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = (
            'user', 'category', 'business_type', 'legal_name', 'display_name', 'logo', 'email', 'mobile', 'address',
            'address_2', 'state', 'country', 'bank_name', 'account_holder_name', 'account_no', 'branch', 'swift_code',
            'website')


class AdminBusinessDocumentListSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='get_business_name')

    class Meta:
        model = BusinessDocument
        fields = ('id', 'business_name', 'document', 'doc_status')


class AdminBusinessDocumentConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDocument
        field = ('id', 'doc_status', 'reject_reason')
