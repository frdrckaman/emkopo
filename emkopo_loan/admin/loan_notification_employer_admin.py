from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanNotificationEmployer


@admin.register(LoanNotificationEmployer)
class LoanNotificationEmployerAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "PaymentReference",
                    "FSPCode",
                    "FSPName",
                    "ProductCode",
                    "ProductName",
                    "FSP1LoanNumber",
                    "ApplicationNumber",
                    "LoanPayoffAmount",
                    "LoanLiquidationDate",
                    "CheckNumber",
                    "FirstName",
                    "MiddleName",
                    "LastName",
                    "VoteCode",
                    "VoteName",
                    "NIN",
                    "DeductionCode",
                    "DeductionDescription",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "PaymentReference",
        "FSPCode",
        "FSPName",
        "ProductCode",
        "ProductName",
        "FSP1LoanNumber",
        "ApplicationNumber",
        "LoanPayoffAmount",
        "LoanLiquidationDate",
        "CheckNumber",
        "FirstName",
        "MiddleName",
        "LastName",
        "VoteCode",
        "VoteName",
        "NIN",
        "DeductionCode",
        "DeductionDescription",
        "RequestType",
        "MessageType",
    )

    search_fields = (
        "CheckNumber",
        "FSPCode",
        "FSP1LoanNumber",
        "ApplicationNumber",
        "ApplicationNumber",
        "PaymentReference",
    )

    list_filter = (

    )
