from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import PartialLoanRepaymentRequest


@admin.register(PartialLoanRepaymentRequest)
class PartialLoanRepaymentRequestAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "CheckNumber",
                    "FirstName",
                    "MiddleName",
                    "LastName",
                    "VoteCode",
                    "VoteName",
                    "DeductionAmount",
                    "DeductionCode",
                    "DeductionName",
                    "DeductionBalance",
                    "FSPCode",
                    "PaymentOption",
                    "Intention",
                    "AmountToPay",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "CheckNumber",
        "FirstName",
        "MiddleName",
        "LastName",
        "VoteCode",
        "VoteName",
        "DeductionAmount",
        "DeductionCode",
        "DeductionName",
        "DeductionBalance",
        "FSPCode",
        "PaymentOption",
        "Intention",
        "AmountToPay",
        "RequestType",
        "MessageType",
    )

    search_fields = (
        "CheckNumber",
    )

    list_filter = (

    )
