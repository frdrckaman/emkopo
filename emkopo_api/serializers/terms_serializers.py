from rest_framework import serializers

from emkopo_product.models import TermsCondition


class TermsConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsCondition
        fields = ['TermsConditionNumber', 'Description', 'TCEffectiveDate']