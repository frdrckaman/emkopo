from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import Fsp


@admin.register(Fsp)
class FspAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "code",
                    "sysName",
                    "FSPBankAccount",
                    "FSPBankAccountName",
                    "SWIFTCode",
                    "MNOChannels",
                    "status",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "name",
        "code",
        "sysName",
        "FSPBankAccount",
        "FSPBankAccountName",
        "SWIFTCode",
        "MNOChannels",
        "status",
    )

    search_fields = (
        "name",
        "code",
        "sysName",
        "SWIFTCode",
        "FSPBankAccount",
    )

    list_filter = (
        "code",
        "status",
    )
