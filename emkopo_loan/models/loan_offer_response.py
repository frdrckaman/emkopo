from django.db import models
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


# for both FSP AND UTUMISH final verification
class LoanOfferResponse(BaseUuidModel):
    ApplicationNumber = models.CharField(
        verbose_name="Application number",
        max_length=8,
    )
    Reason = models.CharField(
        verbose_name="Reason",
        max_length=150,
        blank=True,
        null=True,
    )
    FSPReferenceNumber = models.CharField(
        verbose_name="FSP Reference number",
        max_length=8,
        blank=True,
        null=True,
    )
    LoanNumber = models.CharField(
        verbose_name="Loan Number",
        max_length=20,
        blank=True,
        null=True,
    )
    TotalAmountToPay = models.DecimalField(
        verbose_name="Total Amount To Pay",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    OtherCharges = models.DecimalField(
        verbose_name="Other charges",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    Approval = models.CharField(
        verbose_name="Approval",
        max_length=10,
    )
    MessageType = models.CharField(
        verbose_name="Message Type",
        max_length=100,
    )
    RequestType = models.CharField(
        verbose_name="Request Type",
        max_length=45,
        choices=REQUEST_TYPE,
    )
    status = models.IntegerField(
        verbose_name="Status",
        default=1,
    )

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.ApplicationNumber}'

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Loan Offer Response"
        verbose_name_plural = "Loan Offer Responses"
