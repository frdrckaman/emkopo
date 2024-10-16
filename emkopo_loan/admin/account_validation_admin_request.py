from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import AccountValidationRequest


@admin.register(AccountValidationRequest)
class AccountValidationRequestAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "AccountNumber",
                    "FirstName",
                    "MiddleName",
                    "LastName",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "AccountNumber",
        "FirstName",
        "MiddleName",
        "LastName",
        "RequestType",
        "MessageType",
    )

    search_fields = (
        "AccountNumber",
        "LoanNumber",
    )

    list_filter = (
        "Timestamp",
        "MessageType",
    )
