from rest_framework import serializers

from emkopo_api.serializers import LoanOffersRequestSerializer
from emkopo_loan.models import UserResponse


class UserResponseSerializer(serializers.ModelSerializer):
    ApplicationNumber = LoanOffersRequestSerializer(many=False, read_only=True)

    class Meta:
        model = UserResponse
        fields = [
            'FspComplies', 'FspResponse', 'FSPReferenceNumber', 'ApplicationNumber',
            'LoanNumber', 'TotalAmountToPay', 'OtherCharges', 'Reason',
        ]


