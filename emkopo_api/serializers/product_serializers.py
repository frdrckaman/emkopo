from rest_framework import serializers

from emkopo_api.serializers import TermsConditionSerializer
from emkopo_product.models import ProductCatalog


class ProductCatalogSerializer(serializers.ModelSerializer):
    terms_conditions = TermsConditionSerializer(many=True, read_only=True)

    class Meta:
        model = ProductCatalog
        fields = [
            'ProductCode', 'ProductName', 'ProductDescription', 'ForExecutive',
            'MinimumTenure', 'MaximumTenure', 'InterestRate', 'ProcessFee',
            'Insurance', 'MaxAmount', 'MinAmount', 'RepaymentType', 'Currency',
            'terms_conditions'
        ]
