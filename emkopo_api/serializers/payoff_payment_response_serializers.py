from rest_framework import serializers

from emkopo_loan.models import LoanPayoffPaymentResponse


class LoanPayoffPaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayoffPaymentResponse
        fields = ['LoanNumber', 'TotalPayOffAmount', 'LastDeductionDate', 'FSPBankAccount',
                  'FSPBankAccountName', 'SWIFTCode', 'MNOChannels', 'FinalPaymentDate', 'EndDate']
        extra_kwargs = {
            'LastDeductionDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
            'FinalPaymentDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
            'EndDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
        }

    def validate(self, data):
        # Custom validation logic can be added here
        return data
