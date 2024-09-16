from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanRestructuringRequest


@admin.register(LoanRestructuringRequest)
class LoanRestructuringAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "ApplicationNumber",
                    "LoanNumber",
                    "Comments",
                    "LoanOutstandingAmount",
                    "NewLoanAmount",
                    "NewInstallmentAmount",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "ApplicationNumber",
        "LoanNumber",
        "Comments",
        "LoanOutstandingAmount",
        "NewLoanAmount",
        "NewInstallmentAmount",
    )

    search_fields = (
        "ApplicationNumber",
        "LoanNumber",
    )

    list_filter = (
        "Timestamp",
    )
