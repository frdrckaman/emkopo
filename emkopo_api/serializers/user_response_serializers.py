from rest_framework import serializers

from emkopo_loan.models import UserResponse


class UserResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserResponse
        fields = [
            'FspComplies', 'FspResponse', 'FSPReferenceNumber', 'ApplicationNumber',
            'LoanNumber', 'TotalAmountToPay', 'OtherCharges', 'Reason',
        ]


