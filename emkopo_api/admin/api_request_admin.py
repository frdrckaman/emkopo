from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import ApiRequest


@admin.register(ApiRequest)
class ApiRequestAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "MessageType",
                    "RequestType",
                    "TimeStamp",
                    "ApiUrl",
                    "PayLoad",
                    "Status",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "MessageType",
        "RequestType",
        "TimeStamp",
        "Status",
        "ApiUrl",
        "PayLoad",
    )

    search_fields = (
        "MessageType",
        "RequestType",
        "Status",
    )

    list_filter = (
        "TimeStamp",
    )
