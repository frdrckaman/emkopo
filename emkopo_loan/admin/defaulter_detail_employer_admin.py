from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanDefaulterDetailEmployer


@admin.register(LoanDefaulterDetailEmployer)
class LoanDefaulterDetailEmployerAdmin(BaseSimpleHistoryAdmin):
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
                    "VoteName",
                    "InstallationAmount",
                    "DeductionAmount",
                    "DeductionCode",
                    "DeductionName",
                    "OutstandingBalance",
                    "LastPayDate",
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
        "VoteName",
        "InstallationAmount",
        "DeductionAmount",
        "DeductionCode",
        "DeductionName",
        "OutstandingBalance",
        "LastPayDate",
        "RequestType",
        "MessageType",
    )

    search_fields = (
        "CheckNumber",
        "LoanNumber",
    )

    list_filter = (
        "Timestamp",
    )
