from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanDeductionRecord


@admin.register(LoanDeductionRecord)
class LoanDeductionRecordAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
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
                    "HasStopPay",
                    "DeductionAmount",
                    "StopPayReason",
                    "CheckDate",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
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
        "HasStopPay",
        "DeductionAmount",
        "StopPayReason",
        "CheckDate",
        "MessageType",
        "RequestType",
    )

    search_fields = (
        "CheckNumber",
        "LoanNumber",
    )

    list_filter = (
        "RequestType",
        "Timestamp",
    )
