from django.contrib import admin
from django_audit_fields import audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin as BaseSimpleHistoryAdmin

from ..models import ProductCatalog


@admin.register(ProductCatalog)
class ProductCatalogAdmin(BaseSimpleHistoryAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "ProductCode",
                    "ProductName",
                    "ProductDescription",
                    "ForExecutive",
                    "MinimumTenure",
                    "MaximumTenure",
                    "InterestRate",
                    "ProcessFee",
                    "Insurance",
                    "MaxAmount",
                    "MinAmount",
                    "RepaymentType",
                    "Currency",
                    "status",
                ),
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "ProductCode",
        "ProductName",
        "ProductDescription",
        "ForExecutive",
        "MinimumTenure",
        "MaximumTenure",
        "InterestRate",
        "ProcessFee",
        "Insurance",
        "MaxAmount",
        "MinAmount",
        "RepaymentType",
        "Currency",
        "status",
    )

    search_fields = (
        "ProductCode",
        "ProductName",
        "status",
    )

    list_filter = (
        "ProductCode",
        "ForExecutive",
        "status",
    )
