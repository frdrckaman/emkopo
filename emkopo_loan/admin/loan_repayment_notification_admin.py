from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanRepaymentNotification


@admin.register(LoanRepaymentNotification)
class LoanRepaymentNotificationAdmin(BaseSimpleHistoryAdmin):
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
                    "MaturityDate",
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
        "MaturityDate",
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
        "Timestamp",
    )
