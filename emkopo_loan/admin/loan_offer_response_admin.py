from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanOfferResponse


@admin.register(LoanOfferResponse)
class LoanOfferResponseAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "ApplicationNumber",
                    "LoanNumber",
                    "FSPReferenceNumber",
                    "Approval",
                    "Reason",
                    "TotalAmountToPay",
                    "OtherCharges",
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
        "FSPReferenceNumber",
        "Approval",
        "Reason",
        "TotalAmountToPay",
        "OtherCharges",
        "MessageType",
        "RequestType",
    )

    search_fields = (
        "ApplicationNumber",
        "LoanNumber",
    )

    list_filter = (
        "MessageType",
        "RequestType",
    )
