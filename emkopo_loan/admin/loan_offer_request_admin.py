from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanOfferRequest


@admin.register(LoanOfferRequest)
class LoanOfferRequestAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "CheckNumber",
                    "FirstName",
                    "MiddleName",
                    "LastName",
                    "Sex",
                    "BankAccountNumber",
                    "EmploymentDate",
                    "MaritalStatus",
                    "ConfirmationDate",
                    "TotalEmployeeDeduction",
                    "NearestBranchName",
                    "VoteCode",
                    "VoteName",
                    "NIN",
                    "DesignationCode",
                    "DesignationName",
                    "BasicSalary",
                    "NetSalary",
                    "OneThirdAmount",
                    "RequestedAmount",
                    "DesiredDeductibleAmount",
                    "RetirementDate",
                    "TermsOfEmployment",
                    "Tenure",
                    "ProductCode",
                    "InterestRate",
                    "ProcessingFee",
                    "Insurance",
                    "PhysicalAddress",
                    "TelephoneNumber",
                    "EmailAddress",
                    "MobileNumber",
                    "ApplicationNumber",
                    "LoanPurpose",
                    "ContractStartDate",
                    "ContractEndDate",
                    "LoanNumber",
                    "SettlementAmount",
                    "MessageType",
                    "RequestType",
                    "status",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "ApplicationNumber",
        "LoanNumber",
        "CheckNumber",
        "FirstName",
        "MiddleName",
        "LastName",
        "Sex",
        "BankAccountNumber",
        "BasicSalary",
        "NetSalary",
        "TotalEmployeeDeduction",
        "TermsOfEmployment",
        "MobileNumber",
        "EmailAddress",
        "PhysicalAddress",
        "RequestType",
        "MessageType",
    )

    search_fields = (
        "CheckNumber",
        "ApplicationNumber",
        "LoanNumber",
    )

    list_filter = (
        "MessageType",
        "RequestType",
    )
