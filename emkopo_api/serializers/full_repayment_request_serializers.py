from rest_framework import serializers

from emkopo_loan.models import FullLoanRepaymentRequest


class FullLoanRepaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullLoanRepaymentRequest
        fields = ['CheckNumber', 'LoanNumber', 'FirstName', 'MiddleName', 'LastName',
                  'VoteCode', 'VoteName', 'DeductionAmount', 'DeductionCode', 'DeductionName',
                  'DeductionBalance', 'PaymentOption']

    def validate(self, data):
        # Custom validation logic can be added here
        return data
