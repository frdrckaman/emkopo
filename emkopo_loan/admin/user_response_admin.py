from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import UserResponse


@admin.register(UserResponse)
class UserResponseAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "Staff",
                    "LoanOfferRequest",
                    "FspComplies",
                    "FspResponse",
                    "FSPReferenceNumber",
                    "LoanNumber",
                    "TotalAmountToPay",
                    "OtherCharges",
                    "Reason",
                    "Timestamp",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "LoanOfferRequest",
        "Staff",
        "FspComplies",
        "FspResponse",
        "FSPReferenceNumber",
        "LoanNumber",
        "TotalAmountToPay",
        "OtherCharges",
        "Reason",
        "Timestamp",
    )

    search_fields = (
        "LoanOfferRequest",
        "FSPReferenceNumber",
        "Staff",
        "LoanNumber",
        "Timestamp",
    )

    list_filter = (
        "FspResponse",
        "Timestamp",
    )