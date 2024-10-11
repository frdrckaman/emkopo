from rest_framework import serializers

from emkopo_loan.models import LoanTakeoverDisbursementNotification


class LoanTakeoverDisbursementNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanTakeoverDisbursementNotification
        fields = ['ApplicationNumber', 'FSPReferenceNumber', 'LoanNumber', 'TotalAmountToPay',
                  'DisbursementDate', 'Reason']


    def validate(self, data):
        # Custom validation can be added here, if needed
        return data
