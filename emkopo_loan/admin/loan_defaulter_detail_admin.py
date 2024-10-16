from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import LoanDefaulterDetail


@admin.register(LoanDefaulterDetail)
class LoanDefaulterDetailAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "CheckNumber",
                    "LoanNumber",
                    "FSPCode",
                    "LastPaymentDate",
                    "EmploymentStatus",
                    "PhysicalAddress",
                    "TelephoneNumber",
                    "EmailAddress",
                    "Fax",
                    "MobileNumber",
                    "ContactPerson",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "CheckNumber",
        "LoanNumber",
        "FSPCode",
        "LastPaymentDate",
        "EmploymentStatus",
        "PhysicalAddress",
        "TelephoneNumber",
        "EmailAddress",
        "Fax",
        "MobileNumber",
        "ContactPerson",
        "RequestType",
        "MessageType",
    )

    search_fields = (
        "CheckNumber",
        "LoanNumber",
    )

    list_filter = (
        "MessageType",
        "Timestamp",
    )
