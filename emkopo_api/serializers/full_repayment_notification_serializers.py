from rest_framework import serializers

from emkopo_loan.models import FullLoanRepaymentNotification


class FullLoanRepaymentNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullLoanRepaymentNotification
        fields = ['CheckNumber', 'ApplicationNumber', 'LoanNumber', 'PaymentReference',
                  'DeductionCode', 'PaymentDescription', 'PaymentDate', 'PaymentAmount',
                  'LoanBalance']
        extra_kwargs = {
            'PaymentDate': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},
        }

    def validate(self, data):
        # Custom validation logic can be added here if needed
        return data
