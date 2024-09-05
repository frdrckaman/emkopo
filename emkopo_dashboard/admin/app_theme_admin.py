from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import AppTheme


@admin.register(AppTheme)
class AppThemeAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "theme_mode",
                    "theme_name",
                    "theme_user",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "theme_mode",
        "theme_name",
        "theme_user",
    )

    search_fields = (
        "theme_mode",
        "theme_name",
        "theme_user",
    )

    radio_fields = {
        "theme_mode": admin.VERTICAL,
    }
