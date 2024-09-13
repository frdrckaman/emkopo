from rest_framework import serializers

from emkopo_api.serializers import LoanChargeRequestSerializer
from emkopo_loan.models import LoanChargeResponse


class LoanChargeResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoanChargeResponse
        fields = [
            'DesiredDeductibleAmount',
            'TotalInsurance',
            'TotalProcessingFees',
            'TotalInterestRateAmount',
            'OtherCharges',
            'NetLoanAmount',
            'TotalAmountToPay',
            'Tenure',
            'EligibleAmount',
            'MonthlyReturnAmount',
            'MessageType',
            'RequestType',
            'status',
        ]
