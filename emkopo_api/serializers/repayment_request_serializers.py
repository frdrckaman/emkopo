from rest_framework import serializers

from emkopo_loan.models import LoanRepaymentRequest


class LoanRepaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepaymentRequest
        fields = ['DeductionCode', 'VoteCode', 'VoteName', 'CheckNumber', 'FirstName',
                  'MiddleName', 'LastName', 'PayDate']
        # extra_kwargs = {
        #     'PayDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},  # Handle the datetime format in the XML
        # }

    def validate(self, data):
        # Custom validation logic can be added here, if needed
        return data
