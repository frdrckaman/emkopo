from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanLiquidationRequest


@admin.register(LoanLiquidationRequest)
class LoanLiquidationRequestAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "ProductCode",
                    "LoanAmount",
                    "DeductionAmount",
                    "TakeOverBalance",
                    "FSP1Code",
                    "FSP1Name",
                    "FSP1LoanNumber",
                    "FSP1PaymentReferenceNumber",
                    "NetLoanAmount",
                    "TotalAmountToPay",
                    "PaymentRate",
                    "Reserved3",
                    "TermsAndConditionsNumber",
                    "ApplicationNumber",
                    "FSPReferenceNumber",
                    "ApproverName",
                    "ApproverDesignation",
                    "ApproverWorkstation",
                    "ApproverInstitution",
                    "ActionDateAndTime",
                    "ContactPerson",
                    "ApprovalReferenceNumber",
                    "Status",
                    "Reason",
                    "Comments",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "ApplicationNumber",
        "ProductCode",
        "LoanAmount",
        "DeductionAmount",
        "DeductionAmount",
        "TakeOverBalance",
        "FSP1Code",
        "FSP1Name",
        "FSP1LoanNumber",
        "FSP1PaymentReferenceNumber",
        "NetLoanAmount",
        "TotalAmountToPay",
        "PaymentRate",
        "Reserved3",
        "TermsAndConditionsNumber",
        "FSPReferenceNumber",
        "ApproverName",
        "ApproverDesignation",
        "ApproverWorkstation",
        "ApproverInstitution",
        "ActionDateAndTime",
        "ContactPerson",
        "ApprovalReferenceNumber",
        "Status",
        "Reason",
        "Comments",
        "RequestType",
        "MessageType",
    )

    search_fields = (
        "FSP1LoanNumber",
        "ApplicationNumber",
        "ApplicationNumber",
        "FSPReferenceNumber",
        "FSP1PaymentReferenceNumber",
    )

    list_filter = (

    )
