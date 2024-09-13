from rest_framework import serializers

from emkopo_loan.models import LoanChargeRequest


class HeaderSerializer(serializers.Serializer):
    Sender = serializers.CharField(max_length=100)
    Receiver = serializers.CharField(max_length=100)
    FSPCode = serializers.CharField(max_length=10)
    MsgId = serializers.CharField(max_length=50)
    MessageType = serializers.CharField(max_length=50)


class MessageDetailsSerializer(serializers.Serializer):
    CheckNumber = serializers.CharField(max_length=20)
    DesignationCode = serializers.CharField(max_length=20)
    DesignationName = serializers.CharField(max_length=100)
    BasicSalary = serializers.DecimalField(max_digits=15, decimal_places=2)
    NetSalary = serializers.DecimalField(max_digits=15, decimal_places=2)
    OneThirdAmount = serializers.DecimalField(max_digits=15, decimal_places=2)
    RequestedAmount = serializers.DecimalField(max_digits=15, decimal_places=2)
    DeductibleAmount = serializers.DecimalField(max_digits=15, decimal_places=2)
    DesiredDeductibleAmount = serializers.DecimalField(max_digits=15, decimal_places=2)
    RetirementDate = serializers.CharField(max_length=10)
    TermsOfEmployment = serializers.CharField(max_length=50)
    Tenure = serializers.IntegerField()
    ProductCode = serializers.CharField(max_length=10)
    VoteCode = serializers.CharField(max_length=10)
    TotalEmployeeDeduction = serializers.DecimalField(max_digits=15, decimal_places=2)
    JobClassCode = serializers.CharField(max_length=10)


class LoanChargeRequestDocumentSerializer(serializers.Serializer):
    Header = HeaderSerializer()
    MessageDetails = MessageDetailsSerializer()
    Signature = serializers.CharField(max_length=100)


class LoanChargeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanChargeRequest
        fields = ['CheckNumber', 'DesignationCode', 'DesignationName', 'BasicSalary',
                  'NetSalary', 'OneThirdAmount', 'RequestedAmount', 'DeductibleAmount',
                  'DesiredDeductibleAmount', 'RetirementDate', 'TermsOfEmployment', 'Tenure',
                  'ProductCode', 'VoteCode', 'TotalEmployeeDeduction', 'JobClassCode']
