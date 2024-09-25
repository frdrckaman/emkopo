from rest_framework import serializers

from emkopo_loan.models import LoanOfferRequest


class LoanOfferRequestSerializer(serializers.Serializer):
    CheckNumber = serializers.IntegerField()
    FirstName = serializers.CharField(max_length=30)
    MiddleName = serializers.CharField(max_length=30, required=False, allow_blank=True)
    LastName = serializers.CharField(max_length=30)
    Sex = serializers.CharField(max_length=1, required=False)
    BankAccountNumber = serializers.CharField(max_length=20, required=False)
    EmploymentDate = serializers.DateField(required=False)
    MaritalStatus = serializers.CharField(max_length=10, required=False)
    ConfirmationDate = serializers.CharField(max_length=10, required=False)
    TotalEmployeeDeduction = serializers.DecimalField(max_digits=40, decimal_places=2, required=False)
    NearestBranchName = serializers.CharField(max_length=50, required=False)
    VoteCode = serializers.CharField(max_length=6)
    VoteName = serializers.CharField(max_length=255)
    NIN = serializers.CharField(max_length=22)
    DesignationCode = serializers.CharField(max_length=8)
    DesignationName = serializers.CharField(max_length=255)
    BasicSalary = serializers.DecimalField(max_digits=40, decimal_places=2)
    NetSalary = serializers.DecimalField(max_digits=40, decimal_places=2)
    OneThirdAmount = serializers.DecimalField(max_digits=40, decimal_places=2)
    RequestedAmount = serializers.DecimalField(max_digits=40, decimal_places=2)
    DesiredDeductibleAmount = serializers.DecimalField(max_digits=40, decimal_places=2,
                                                       required=False)
    RetirementDate = serializers.CharField(max_length=12, required=False)
    TermsOfEmployment = serializers.CharField(max_length=30)
    Tenure = serializers.IntegerField()
    ProductCode = serializers.CharField(max_length=8)
    InterestRate = serializers.DecimalField(max_digits=40, decimal_places=2)
    ProcessingFee = serializers.DecimalField(max_digits=40, decimal_places=2)
    Insurance = serializers.DecimalField(max_digits=40, decimal_places=2)
    PhysicalAddress = serializers.CharField(max_length=50, required=False)
    EmailAddress = serializers.CharField(max_length=50, required=False)
    MobileNumber = serializers.CharField(max_length=12, required=False)
    ApplicationNumber = serializers.CharField(max_length=12)
    LoanPurpose = serializers.CharField(max_length=250, required=False)
    ContractStartDate = serializers.DateField(required=False)
    ContractEndDate = serializers.DateField(required=False)

    FSP1Code = serializers.CharField(max_length=50, required=False)
    FSP1LoanNumber = serializers.CharField(max_length=50, required=False)
    TakeOverBalance = serializers.DecimalField(max_digits=40, decimal_places=2, required=False)
    FSP1EndDate = serializers.DateTimeField(required=False)
    FSP1LastDeductionDate = serializers.DateTimeField(required=False)
    FSP1BankAccount = serializers.CharField(max_length=50, required=False)
    FSP1BankAccountName = serializers.CharField(max_length=100, required=False)
    FSP1SWIFTCode = serializers.CharField(max_length=50, required=False)
    FSP1MNOChannels = serializers.CharField(max_length=50, required=False)
    FSP1PaymentReferenceNumber = serializers.CharField(max_length=50, required=False)
    FSP1FinalPaymentDate = serializers.DateTimeField(required=False)
    Signature = serializers.CharField(max_length=255)


class LoanOffersRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOfferRequest
        fields = [
            'CheckNumber', 'FirstName', 'MiddleName', 'LastName', 'Sex', 'BankAccountNumber',
            'EmploymentDate', 'MaritalStatus', 'ConfirmationDate', 'TotalEmployeeDeduction',
            'NearestBranchName', 'VoteCode', 'VoteName', 'NIN', 'DesignationCode',
            'DesignationName', 'BasicSalary', 'NetSalary', 'OneThirdAmount', 'RequestedAmount',
            'DesiredDeductibleAmount', 'RetirementDate', 'TermsOfEmployment', 'Tenure',
            'ProductCode', 'InterestRate', 'ProcessingFee', 'Insurance', 'PhysicalAddress',
            'TelephoneNumber', 'EmailAddress', 'MobileNumber', 'ApplicationNumber',
            'LoanPurpose', 'ContractStartDate', 'ContractEndDate', 'LoanNumber',
            'SettlementAmount', 'LoanOfferType', 'FSP1Code', 'FSP1LoanNumber',
            'TakeOverBalance', 'FSP1EndDate', 'FSP1LastDeductionDate', 'FSP1BankAccount',
            'FSP1BankAccountName', 'FSP1SWIFTCode', 'FSP1MNOChannels',
            'FSP1PaymentReferenceNumber', 'FSP1FinalPaymentDate', 'MessageType', 'RequestType'
        ]
