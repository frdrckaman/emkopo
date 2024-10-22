from rest_framework import serializers

from emkopo_loan.models import LoanDefaulterDetail


class LoanDefaulterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDefaulterDetail
        fields = ['CheckNumber', 'LoanNumber', 'FSPCode', 'LastPaymentDate', 'EmploymentStatus',
                  'PhysicalAddress', 'TelephoneNumber', 'EmailAddress', 'Fax', 'MobileNumber',
                  'ContactPerson']
        extra_kwargs = {
            'LastPaymentDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
        }

    def validate(self, data):
        return data
