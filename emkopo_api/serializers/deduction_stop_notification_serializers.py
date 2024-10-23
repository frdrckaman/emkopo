from rest_framework import serializers

from emkopo_loan.models import LoanDeductionStopNotification


class LoanDeductionStopNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDeductionStopNotification
        fields = ['FSPReferenceNumber', 'LoanNumber', 'CheckNumber', 'FirstName', 'MiddleName', 'LastName',
                  'NationalId', 'VoteCode', 'VoteName', 'DepartmentCode', 'DepartmentName',
                  'DeductionCode', 'DeductionDescription', 'BalanceAmount', 'DeductionAmount',
                  'StopDate', 'StopReason']
