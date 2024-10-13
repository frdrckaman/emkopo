from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanRepaymentRequest


@admin.register(LoanRepaymentRequest)
class LoanRepaymentRequestAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "CheckNumber",
                    "DeductionCode",
                    "VoteCode",
                    "VoteName",
                    "FirstName",
                    "MiddleName",
                    "LastName",
                    "PayDate",
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
        "DeductionCode",
        "VoteCode",
        "VoteName",
        "FirstName",
        "MiddleName",
        "LastName",
        "PayDate",
        "MessageType",
        "RequestType",
    )

    search_fields = (
        "CheckNumber",
        "DeductionCode",
    )

    list_filter = (
        "MessageType",
        "RequestType",
    )
