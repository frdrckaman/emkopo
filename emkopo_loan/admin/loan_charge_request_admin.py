from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanChargeRequest


@admin.register(LoanChargeRequest)
class LoanChargeRequestAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "CheckNumber",
                    "DesignationCode",
                    "DesignationName",
                    "BasicSalary",
                    "NetSalary",
                    "OneThirdAmount",
                    "RequestedAmount",
                    "DeductibleAmount",
                    "DesiredDeductibleAmount",
                    "RetirementDate",
                    "TermsOfEmployment",
                    "Tenure",
                    "ProductCode",
                    "VoteCode",
                    "TotalEmployeeDeduction",
                    "JobClassCode",
                    "MessageType",
                    "RequestType",
                    "status",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "CheckNumber",
        "DesignationCode",
        "DesignationName",
        "BasicSalary",
        "NetSalary",
        "OneThirdAmount",
        "RequestedAmount",
        "DeductibleAmount",
        "DesiredDeductibleAmount",
        "RetirementDate",
        "TermsOfEmployment",
        "Tenure",
        "ProductCode",
        "VoteCode",
        "TotalEmployeeDeduction",
        "JobClassCode",
        "MessageType",
        "RequestType",
    )

    search_fields = (
        "CheckNumber",
    )

    list_filter = (
        "MessageType",
        "RequestType",
    )
