from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import FullLoanRepaymentNotification


@admin.register(FullLoanRepaymentNotification)
class FullLoanRepaymentNotificationAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "CheckNumber",
                    "ApplicationNumber",
                    "LoanNumber",
                    "PaymentReference",
                    "DeductionCode",
                    "PaymentDescription",
                    "PaymentDate",
                    "PaymentAmount",
                    "LoanBalance",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "CheckNumber",
        "ApplicationNumber",
        "LoanNumber",
        "PaymentReference",
        "DeductionCode",
        "PaymentDescription",
        "PaymentDate",
        "PaymentAmount",
        "LoanBalance",
        "RequestType",
        "MessageType",
    )

    search_fields = (
        "CheckNumber",
        "ApplicationNumber",
        "PaymentReference",
    )

    list_filter = (

    )
