from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class FullLoanRepaymentNotification(BaseUuidModel):
    CheckNumber = models.CharField(
        verbose_name="CheckNumber",
        max_length=45,
    )
    ApplicationNumber = models.CharField(
        verbose_name="First Name",
        max_length=45,
    )
    LoanNumber = models.CharField(
        verbose_name="Middle Name",
        max_length=45,
    )
    PaymentReference = models.CharField(
        verbose_name="Last Name",
        max_length=45,
    )
    DeductionCode = models.DateTimeField(
        verbose_name="Payment Date",
    )
    PaymentDescription = models.CharField(
        verbose_name="Payment Description",
        max_length=125,
    )
    PaymentDate = models.DateTimeField(
        verbose_name="Payment Date",
    )
    PaymentAmount = models.DecimalField(
        verbose_name="Payment Amount",
        decimal_places=2,
        max_digits=40,
    )
    LoanBalance = models.DecimalField(
        verbose_name="Loan Balance",
        decimal_places=2,
        max_digits=40,
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
    status = models.IntegerField(
        verbose_name="Status",
        default=1,
    )

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.CheckNumber}'

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Ful Loan Repayment Notification"
        verbose_name_plural = "Full Loan Repayment Notifications"
