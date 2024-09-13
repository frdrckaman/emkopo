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
        "Timestamp",
    )

    search_fields = (
        "LoanOfferRequest",
        "Staff",
        "Timestamp",
    )

    list_filter = (
        "Timestamp",
    )
