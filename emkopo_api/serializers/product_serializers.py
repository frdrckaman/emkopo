from rest_framework import serializers

from emkopo_api.serializers import TermsConditionSerializer


class ProductCatalogSerializer(serializers.Serializer):
    ProductCode = serializers.CharField(max_length=8)
    ProductName = serializers.CharField(max_length=255)
    ProductDescription = serializers.CharField(max_length=255, required=False)
    ForExecutive = serializers.BooleanField()
    MinimumTenure = serializers.IntegerField()
    MaximumTenure = serializers.IntegerField()
    InterestRate = serializers.DecimalField(max_digits=5, decimal_places=2)
    ProcessFee = serializers.DecimalField(max_digits=5, decimal_places=2, required=False)
    Insurance = serializers.DecimalField(max_digits=5, decimal_places=2)
    MaxAmount = serializers.DecimalField(max_digits=40, decimal_places=2)
    MinAmount = serializers.DecimalField(max_digits=40, decimal_places=2)
    RepaymentType = serializers.CharField(max_length=10, required=False)
    Currency = serializers.CharField(max_length=10)
    TermsCondition = TermsConditionSerializer(many=True)
