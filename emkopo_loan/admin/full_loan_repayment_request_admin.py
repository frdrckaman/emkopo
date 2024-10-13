from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import FullLoanRepaymentRequest


@admin.register(FullLoanRepaymentRequest)
class FullLoanRepaymentRequestAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "CheckNumber",
                    "LoanNumber",
                    "FirstName",
                    "MiddleName",
                    "LastName",
                    "VoteCode",
                    "VoteName",
                    "DeductionAmount",
                    "DeductionCode",
                    "DeductionName",
                    "DeductionBalance",
                    "PaymentOption",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "CheckNumber",
        "LoanNumber",
        "FirstName",
        "MiddleName",
        "LastName",
        "VoteCode",
        "VoteName",
        "DeductionAmount",
        "DeductionCode",
        "DeductionName",
        "DeductionBalance",
        "PaymentOption",
        "RequestType",
        "MessageType",
    )

    search_fields = (
        "CheckNumber",
        "LoanNumber",
    )

    list_filter = (

    )
