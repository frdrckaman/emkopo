from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanChargeResponse


@admin.register(LoanChargeResponse)
class LoanChargeResponseAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "LoanChargeRequest",
                    "DesiredDeductibleAmount",
                    "TotalInsurance",
                    "TotalProcessingFees",
                    "TotalInterestRateAmount",
                    "OtherCharges",
                    "NetLoanAmount",
                    "TotalAmountToPay",
                    "Tenure",
                    "EligibleAmount",
                    "MonthlyReturnAmount",
                    "MessageType",
                    "RequestType",
                    "status",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "LoanChargeRequest",
        "DesiredDeductibleAmount",
        "TotalInsurance",
        "TotalProcessingFees",
        "TotalInterestRateAmount",
        "OtherCharges",
        "NetLoanAmount",
        "TotalAmountToPay",
        "Tenure",
        "EligibleAmount",
        "MonthlyReturnAmount",
        "MessageType",
        "RequestType",
    )

    search_fields = (
        "",
    )

    list_filter = (
        "MessageType",
        "RequestType",
    )
