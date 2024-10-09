from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanLiquidationNotification


@admin.register(LoanLiquidationNotification)
class LoanLiquidationNotificationAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "PaymentReference",
                    "ApplicationNumber",
                    "ApproverName",
                    "ApproverDesignation",
                    "ApproverWorkstation",
                    "ApproverInstitution",
                    "ActionDateAndTime",
                    "ContactPerson",
                    "MonthlyPrincipal",
                    "MonthlyInterest",
                    "MonthlyInstalment",
                    "OutstandingBalance",
                    "DeductionStartDate",
                    "DeductionEndDate",
                    "FSPReferenceNumber",
                    "CheckNumber",
                    "FirstName",
                    "MiddleName",
                    "LastName",
                    "VoteCode",
                    "VoteName",
                    "NIN",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "PaymentReference",
        "ApplicationNumber",
        "ApproverName",
        "ApproverDesignation",
        "ApproverWorkstation",
        "ApproverInstitution",
        "ActionDateAndTime",
        "ContactPerson",
        "MonthlyPrincipal",
        "MonthlyInterest",
        "MonthlyInstalment",
        "OutstandingBalance",
        "DeductionStartDate",
        "DeductionEndDate",
        "FSPReferenceNumber",
        "CheckNumber",
        "FirstName",
        "MiddleName",
        "LastName",
        "VoteCode",
        "VoteName",
        "NIN",
    )

    search_fields = (
        "CheckNumber",
        "ApplicationNumber",
        "PaymentReference",
    )

    list_filter = (

    )
