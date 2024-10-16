from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import AccountValidationResponse


@admin.register(AccountValidationResponse)
class AccountValidationResponseAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "Valid",
                    "Reason",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "Valid",
        "Reason",
        "RequestType",
        "MessageType",
    )

    search_fields = (

    )

    list_filter = (
        "Timestamp",
        "MessageType",
    )
