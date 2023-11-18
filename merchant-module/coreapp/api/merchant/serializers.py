from rest_framework import serializers

from coreapp.models import BusinessDocument, Business


class MerchantBusinessCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = (
            'user', 'category', 'business_type', 'legal_name', 'display_name', 'logo', 'email', 'mobile', 'address',
            'address_2', 'state', 'country', 'bank_name', 'account_holder_name', 'account_no', 'branch', 'swift_code',
            'website')


class MerchantBusinessDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessDocument
        fields = ('business', 'document', 'doc_type', 'doc_status')


class MerchantLegalDocumentUploadSerializer(serializers.Serializer):
    business_document = MerchantBusinessDocumentSerializer(many=True)

    def create(self, validated_data):
        business_document = validated_data.pop('business_document_serializer')

        for doc in business_document:
            document = BusinessDocument.objects.create(**doc)
            document.save()
            return document
