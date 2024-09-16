from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class LoanPayOffBalanceRequest(BaseUuidModel):
    CheckNumber = models.IntegerField(
        verbose_name="Check number",
    )
    LoanNumber = models.CharField(
        verbose_name="Loan Number",
        max_length=20,
    )
    FirstName = models.CharField(
        verbose_name="First Name",
        max_length=30,
    )
    MiddleName = models.CharField(
        verbose_name="Middle Name",
        max_length=30,
    )
    LastName = models.CharField(
        verbose_name="Last Name",
        max_length=30,
    )
    VoteCode = models.CharField(
        verbose_name="Vote code",
        max_length=6,
    )
    VoteName = models.CharField(
        verbose_name="Vote name",
        max_length=255,
    )
    DeductionAmount = models.DecimalField(
        verbose_name="Deduction Amount",
        max_digits=40,
        decimal_places=2,
    )
    DeductionCode = models.CharField(
        verbose_name="Deduction Code",
        max_length=8,
    )
    DeductionName = models.CharField(
        verbose_name="Deduction Name",
        max_length=255,
    )
    DeductionBalance = models.DecimalField(
        verbose_name="Deduction Balance",
        max_digits=40,
        decimal_places=2,
    )
    PaymentOption = models.CharField(
        verbose_name="Other Charges",
        max_length=50,
    )
    Timestamp = models.DateTimeField(
        verbose_name="Timestamp",
        default=timezone.now
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

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.CheckNumber} : {self.LoanNumber}'

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Payoff Balance Request"
        verbose_name_plural = "Payoff Balance Requests"
