from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import PartialLoanRepaymentResponse


@admin.register(PartialLoanRepaymentResponse)
class PartialLoanRepaymentResponseAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "LoanNumber",
                    "TotalPayOffAmount",
                    "LastDeductionDate",
                    "FSPBankAccount",
                    "FSPBankAccountName",
                    "SWIFTCode",
                    "MNOChannels",
                    "PaymentReferenceNumber",
                    "FinalPaymentDate",
                    "EndDate",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "LoanNumber",
        "TotalPayOffAmount",
        "LastDeductionDate",
        "FSPBankAccount",
        "FSPBankAccountName",
        "SWIFTCode",
        "MNOChannels",
        "PaymentReferenceNumber",
        "FinalPaymentDate",
        "EndDate",
    )

    search_fields = (
        "LoanNumber",
        "PaymentReferenceNumber",
    )

    list_filter = (
        "Timestamp",
    )
