from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import Currency


@admin.register(Currency)
class CurrencyAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "code",
                    "status",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "name",
        "code",
        "status",
    )

    search_fields = (
        "name",
        "code",
        "status",
    )

    list_filter = (
        "code",
        "status",
    )
