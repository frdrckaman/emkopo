from rest_framework import serializers

from emkopo_loan.models import LoanRepaymentNotification


class LoanRepaymentNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepaymentNotification
        fields = ['CheckNumber', 'ApplicationNumber', 'LoanNumber', 'PaymentReference',
                  'DeductionCode', 'PaymentDescription', 'PaymentDate', 'MaturityDate',
                  'PaymentAmount', 'LoanBalance']
        extra_kwargs = {
            'PaymentDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
            'MaturityDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S'], 'allow_null': True},
        }

    def validate(self, data):
        # Custom validation logic can be added here
        return data
