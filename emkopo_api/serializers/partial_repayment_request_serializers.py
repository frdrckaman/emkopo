from rest_framework import serializers

from emkopo_loan.models import PartialLoanRepaymentRequest


class PartialLoanRepaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartialLoanRepaymentRequest
        fields = ['CheckNumber', 'FirstName', 'MiddleName', 'LastName',
                  'VoteCode', 'VoteName', 'DeductionAmount', 'DeductionCode', 'DeductionName',
                  'DeductionBalance', 'FSPCode', 'PaymentOption', 'Intention', 'AmountToPay']

    def validate(self, data):
        # Custom validation logic can be added here
        return data
