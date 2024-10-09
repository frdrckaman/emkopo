from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanTakeoverDisbursementNotification


@admin.register(LoanTakeoverDisbursementNotification)
class LoanTakeoverDisbursementNotificationAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "ApplicationNumber",
                    "FSPReferenceNumber",
                    "LoanNumber",
                    "TotalAmountToPay",
                    "DisbursementDate",
                    "Reason",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "ApplicationNumber",
        "FSPReferenceNumber",
        "LoanNumber",
        "TotalAmountToPay",
        "DisbursementDate",
        "Reason",
    )

    search_fields = (
        "LoanNumber",
        "ApplicationNumber",
        "FSPReferenceNumber",
    )

    list_filter = (

    )
