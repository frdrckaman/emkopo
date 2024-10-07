from rest_framework import serializers

from emkopo_loan.models import LoanLiquidationRequest


class LoanLiquidationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanLiquidationRequest
        fields = ['ProductCode', 'LoanAmount', 'DeductionAmount', 'TakeOverBalance', 'FSP1Code',
                  'FSP1Name', 'FSP1LoanNumber', 'FSP1PaymentReferenceNumber', 'NetLoanAmount',
                  'TotalAmountToPay', 'PaymentRate', 'Reserved3', 'TermsAndConditionsNumber',
                  'ApplicationNumber', 'FSPReferenceNumber', 'ApproverName',
                  'ApproverDesignation', 'ApproverWorkstation', 'ApproverInstitution',
                  'ActionDateAndTime', 'ContactPerson', 'ApprovalReferenceNumber', 'Status',
                  'Reason', 'Comments']
        extra_kwargs = {
            'ActionDateAndTime': {'input_formats': ['%Y-%m-%dT%H:%M:%S']},  # Specify the format for datetime
        }

    def validate(self, data):
        """
        Perform custom validation, if needed.
        """
        # Add any custom validation rules here
        # For example, checking if loan amounts are positive
        if data['LoanAmount'] <= 0:
            raise serializers.ValidationError("LoanAmount must be greater than zero.")
        if data['TotalAmountToPay'] <= 0:
            raise serializers.ValidationError("TotalAmountToPay must be greater than zero.")
        return data
