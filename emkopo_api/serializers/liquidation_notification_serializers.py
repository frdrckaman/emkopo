from rest_framework import serializers

from emkopo_loan.models import LoanLiquidationNotification


class LoanLiquidationNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanLiquidationNotification
        fields = ['PaymentReference', 'ApplicationNumber', 'ApproverName', 'ApproverDesignation',
                  'ApproverWorkstation', 'ApproverInstitution', 'ActionDateAndTime', 'ContactPerson',
                  'MonthlyPrincipal', 'MonthlyInterest', 'MonthlyInstalment', 'OutstandingBalance',
                  'DeductionStartDate', 'DeductionEndDate', 'FSPReferenceNumber', 'CheckNumber',
                  'FirstName', 'MiddleName', 'LastName', 'VoteCode', 'VoteName', 'NIN']

    def validate(self, data):
        """
        Perform custom validation, if needed.
        """
        # Example: ensure MonthlyPrincipal and OutstandingBalance are positive values
        if data.get('MonthlyPrincipal') <= 0:
            raise serializers.ValidationError("MonthlyPrincipal must be a positive value.")
        if data.get('OutstandingBalance') < 0:
            raise serializers.ValidationError("OutstandingBalance cannot be negative.")
        return data
