from django.db import models
from simple_history.models import HistoricalRecords

from emkopo_mixins.model import BaseUuidModel
from .product_catalog import ProductCatalog


class TermsCondition(BaseUuidModel):
    ProductCatalog = models.ForeignKey(
        ProductCatalog,
        on_delete=models.CASCADE,
        related_name='terms_conditions',
        verbose_name='Product Catalog'
    )
    TermsConditionNumber = models.CharField(
        verbose_name="Terms Condition Number",
        max_length=20,
    )
    Description = models.CharField(
        verbose_name="Description",
        max_length=255,
    )
    TCEffectiveDate = models.DateField(
        verbose_name="TC Effective Date",
    )
    status = models.BooleanField(
        verbose_name="Status",
        default=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.TermsConditionNumber

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Terms and Condition"
        verbose_name_plural = "Terms and Conditions"
