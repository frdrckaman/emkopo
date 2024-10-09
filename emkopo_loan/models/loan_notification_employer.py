from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class LoanNotificationEmployer(BaseUuidModel):
    PaymentReference = models.CharField(
        verbose_name="Payment Reference",
        max_length=45,
    )
    FSPCode = models.CharField(
        verbose_name="FSP Code",
        max_length=45,
    )
    FSPName = models.CharField(
        verbose_name="FSP Name",
        max_length=120,
    )
    ProductCode = models.IntegerField(
        verbose_name="Product Code",
    )
    ProductName = models.CharField(
        verbose_name="Product Name",
        max_length=255,
    )
    FSP1LoanNumber = models.CharField(
        verbose_name="FSP1 Loan Number",
        max_length=45,
    )
    ApplicationNumber = models.CharField(
        verbose_name="Application Number",
        max_length=45,
    )
    LoanPayoffAmount = models.DecimalField(
        verbose_name="Loan Payoff Amount",
        decimal_places=2,
        max_digits=40,
    )
    LoanLiquidationDate = models.DateField(
        verbose_name="Loan Liquidation Date",
    )
    CheckNumber = models.CharField(
        verbose_name="Check Number",
        max_length=45,
    )
    FirstName = models.CharField(
        verbose_name="First Name",
        max_length=45,
    )
    MiddleName = models.CharField(
        verbose_name="Middle Name",
        max_length=45,
    )
    LastName = models.CharField(
        verbose_name="Last Name",
        max_length=45,
    )
    VoteCode = models.CharField(
        verbose_name="Vote Code",
        max_length=45,
    )
    VoteName = models.CharField(
        verbose_name="Vote Name",
        max_length=45,
    )
    NIN = models.CharField(
        verbose_name="NIN",
        max_length=45,
    )
    DeductionCode = models.CharField(
        verbose_name="Deduction Code",
        max_length=45,
    )
    DeductionDescription = models.CharField(
        verbose_name="Deduction Description",
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
        return f'{self.PaymentReference} : {self.ApplicationNumber}'

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Loan Notification Employer"
        verbose_name_plural = "Loan Notification Employer"
