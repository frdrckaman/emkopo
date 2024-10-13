from rest_framework import serializers

from emkopo_loan.models import LoanRepaymentOffBalanceRequest


class LoanRepaymentOffBalanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepaymentOffBalanceRequest
        fields = ['LoanNumber', 'TotalPayoffAmount', 'FSPBankAccount', 'FSPBankAccountName',
                  'SWIFTCode', 'MNOChannels', 'FinalPaymentDate', 'LastDeductionDate', 'EndDate']
        extra_kwargs = {
            'LastDeductionDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
            'FinalPaymentDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
            'EndDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
        }

    def validate(self, data):
        # Custom validation logic can be added here
        return data
