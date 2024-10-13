from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanRepaymentOffBalanceRequest


@admin.register(LoanRepaymentOffBalanceRequest)
class LoanRepaymentOffBalanceRequestAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "LoanNumber",
                    "TotalPayoffAmount",
                    "FSPBankAccount",
                    "FSPBankAccountName",
                    "SWIFTCode",
                    "MNOChannels",
                    "FinalPaymentDate",
                    "LastDeductionDate",
                    "EndDate",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "LoanNumber",
        "TotalPayoffAmount",
        "FSPBankAccount",
        "FSPBankAccountName",
        "SWIFTCode",
        "MNOChannels",
        "FinalPaymentDate",
        "LastDeductionDate",
        "EndDate",
    )

    search_fields = (
        "LoanNumber",
    )

    list_filter = (
        "Timestamp",
    )
