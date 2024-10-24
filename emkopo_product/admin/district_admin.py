from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import District


@admin.register(District)
class DistrictAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "DistrictNane",
                    "DistrictCode",
                    "active",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "DistrictNane",
        "DistrictCode",
        "active",
    )

    search_fields = (
        "DistrictCode",
        "active",
    )

    list_filter = (
        "active",
    )
