from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import TermsCondition


@admin.register(TermsCondition)
class TermsConditionAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "ProductCatalog",
                    "TermsConditionNumber",
                    "Description",
                    "TCEffectiveDate",
                    "status",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "ProductCatalog",
        "TermsConditionNumber",
        "Description",
        "TCEffectiveDate",
        "status",
    )

    search_fields = (
        "TermsConditionNumber",
        "status",
    )

    list_filter = (
        "ProductCatalog",
        "status",
    )
