from rest_framework import serializers

from emkopo_loan.models import LoanDefaulterDetailEmployer


class LoanDefaulterDetailEmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDefaulterDetailEmployer
        fields = ['CheckNumber', 'LoanNumber', 'VoteName', 'FirstName', 'MiddleName',
                  'LastName', 'InstallationAmount', 'DeductionAmount', 'DeductionCode', 'DeductionName', 'OutstandingBalance', 'LastPayDate']
        extra_kwargs = {
            'LastPayDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
        }

    def validate(self, data):
        # Custom validation logic can be added here
        return data
