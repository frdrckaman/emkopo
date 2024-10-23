from rest_framework import serializers

from emkopo_loan.models import LoanDeductionRecord


class LoanDeductionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDeductionRecord
        fields = ['LoanNumber', 'CheckNumber', 'FirstName', 'MiddleName', 'LastName',
                  'NationalId', 'VoteCode', 'VoteName', 'DepartmentCode', 'DepartmentName',
                  'DeductionCode', 'DeductionDescription', 'BalanceAmount', 'DeductionAmount',
                  'HasStopPay', 'StopPayReason', 'CheckDate']