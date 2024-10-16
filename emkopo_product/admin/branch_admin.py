from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import Branch


@admin.register(Branch)
class BranchAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "District",
                    "BranchCode",
                    "BranchName",
                    "active",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "District",
        "BranchCode",
        "BranchName",
        "active",
    )

    search_fields = (
        "BranchCode",
        "active",
    )

    list_filter = (
        "active",
    )
