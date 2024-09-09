from rest_framework import serializers


class TermsConditionSerializer(serializers.Serializer):
    TermsConditionNumber = serializers.CharField(max_length=20)
    Description = serializers.CharField(max_length=255)
    TCEffectiveDate = serializers.DateField()