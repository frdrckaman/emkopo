from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanTakeoverDetail


@admin.register(LoanTakeoverDetail)
class LoanTakeoverDetailAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "LoanNumber",
                    "FSPReferenceNumber",
                    "PaymentReferenceNumber",
                    "TotalPayoffAmount",
                    "OutstandingBalance",
                    "FSPBankAccount",
                    "FSPBankAccountName",
                    "SWIFTCode",
                    "MNOChannels",
                    "FinalPaymentDate",
                    "LastDeductionDate",
                    "LastPayDate",
                    "EndDate",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "LoanNumber",
        "FSPReferenceNumber",
        "PaymentReferenceNumber",
        "TotalPayoffAmount",
        "OutstandingBalance",
        "FSPBankAccount",
        "FSPBankAccountName",
        "SWIFTCode",
        "MNOChannels",
        "FinalPaymentDate",
        "LastDeductionDate",
        "LastPayDate",
        "EndDate",
    )

    search_fields = (
        "FSPReferenceNumber",
        "PaymentReferenceNumber",
        "LoanNumber",
    )

    list_filter = (
        "Timestamp",
    )
