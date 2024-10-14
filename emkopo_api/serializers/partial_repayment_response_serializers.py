from rest_framework import serializers

from emkopo_loan.models import PartialLoanRepaymentResponse


class PartialLoanRepaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartialLoanRepaymentResponse
        fields = ['LoanNumber', 'TotalPayOffAmount', 'LastDeductionDate', 'FSPBankAccount',
                  'FSPBankAccountName', 'SWIFTCode', 'MNOChannels', 'PaymentReferenceNumber',
                  'FinalPaymentDate', 'EndDate']
        extra_kwargs = {
            'LastDeductionDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
            'FinalPaymentDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
            'EndDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
        }

    def validate(self, data):
        # Custom validation logic can be added here
        return data
