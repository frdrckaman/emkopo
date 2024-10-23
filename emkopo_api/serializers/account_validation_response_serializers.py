from rest_framework import serializers

from emkopo_loan.models import AccountValidationResponse


class AccountValidationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountValidationResponse
        fields = ['AccountNumber', 'Valid', 'Reason']
