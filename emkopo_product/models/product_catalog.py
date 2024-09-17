from django.db import models
from simple_history.models import HistoricalRecords

from emkopo_mixins.model import BaseUuidModel


class ProductCatalog(BaseUuidModel):
    ProductCode = models.CharField(
        verbose_name="Product code",
        max_length=8,
    )
    ProductName = models.CharField(
        verbose_name="Product name",
        max_length=255,
    )
    ProductDescription = models.CharField(
        verbose_name="Product Description",
        max_length=255,
        blank=True,
        null=True,
    )
    ForExecutive = models.BooleanField(
        verbose_name="For Executive",
    )
    MinimumTenure = models.IntegerField(
        verbose_name="Minimum Tenure",
    )
    MaximumTenure = models.IntegerField(
        verbose_name="Maximum Tenure",
    )
    InterestRate = models.DecimalField(
        verbose_name="Interest Rate",
        max_digits=5,
        decimal_places=2,
    )
    ProcessFee = models.DecimalField(
        verbose_name="Process Fee",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    Insurance = models.DecimalField(
        verbose_name="Insurance",
        max_digits=5,
        decimal_places=2,
    )
    MaxAmount = models.DecimalField(
        verbose_name="Maximum Amount",
        max_digits=40,
        decimal_places=2,
    )
    MinAmount = models.DecimalField(
        verbose_name="Minimum Amount",
        max_digits=40,
        decimal_places=2,
    )
    RepaymentType = models.CharField(
        verbose_name="Repayment Type",
        max_length=10,
        blank=True,
        null=True,
    )
    Currency = models.CharField(
        verbose_name="Currency",
        max_length=10,
    )
    status = models.BooleanField(
        verbose_name="Product Catalog Status",
        default=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.ProductCode} - {self.ProductName}"

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Product Catalog"
        verbose_name_plural = "Product Catalog"
