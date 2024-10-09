from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class LoanTakeoverDisbursementNotification(BaseUuidModel):
    ApplicationNumber = models.CharField(
        verbose_name="Application Number",
        max_length=45,
    )
    FSPReferenceNumber = models.CharField(
        verbose_name="FSPReferenceNumber",
        max_length=45,
    )
    LoanNumber = models.CharField(
        verbose_name="LoanNumber",
        max_length=45,
    )
    TotalAmountToPay = models.DecimalField(
        verbose_name="Total Amount To Pay",
        max_digits=40,
        decimal_places=2,
    )
    DisbursementDate = models.DateTimeField(
        verbose_name="Disbursement Date",
    )
    Reason = models.CharField(
        verbose_name="Reason",
        max_length=120,
    )
    status = models.IntegerField(
        verbose_name="Status",
        default=1,
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
    Timestamp = models.DateTimeField(
        verbose_name="Timestamp",
        default=timezone.now
    )

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.FSPReferenceNumber} : {self.ApplicationNumber}'

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Loan Takeover Disbursement Notification"
        verbose_name_plural = "Loan Takeover Disbursement Notification"
