from rest_framework import serializers

from emkopo_loan.models import AccountValidationRequest


class AccountValidationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountValidationRequest
        fields = ['AccountNumber', 'FirstName', 'MiddleName', 'LastName']
