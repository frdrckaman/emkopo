from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanDeductionStopNotification


@admin.register(LoanDeductionStopNotification)
class LoanDeductionStopNotificationAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "FSPReferenceNumber",
                    "LoanNumber",
                    "CheckNumber",
                    "FirstName",
                    "MiddleName",
                    "LastName",
                    "NationalId",
                    "VoteCode",
                    "VoteName",
                    "DepartmentCode",
                    "DepartmentName",
                    "DeductionCode",
                    "BalanceAmount",
                    "DeductionDescription",
                    "DeductionAmount",
                    "StopDate",
                    "StopPayReason",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "FSPReferenceNumber",
        "LoanNumber",
        "CheckNumber",
        "FirstName",
        "MiddleName",
        "LastName",
        "NationalId",
        "VoteCode",
        "VoteName",
        "DepartmentCode",
        "DepartmentName",
        "DeductionCode",
        "BalanceAmount",
        "DeductionDescription",
        "DeductionAmount",
        "StopDate",
        "StopPayReason",
        "MessageType",
        "RequestType",
    )

    search_fields = (
        "FSPReferenceNumber",
        "CheckNumber",
        "LoanNumber",
    )

    list_filter = (
        "RequestType",
        "Timestamp",
    )
