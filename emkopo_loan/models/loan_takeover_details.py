from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class LoanTakeoverDetail(BaseUuidModel):
    LoanNumber = models.CharField(
        verbose_name="Loan Number",
        max_length=20,
    )
    FSPReferenceNumber = models.CharField(
        verbose_name="FSP Reference Number",
        max_length=45,
    )
    PaymentReferenceNumber = models.CharField(
        verbose_name="Payment Reference Number",
        max_length=45,
    )
    TotalPayoffAmount = models.DecimalField(
        verbose_name="Total Payoff Amount",
        max_digits=40,
        decimal_places=2,
    )
    OutstandingBalance = models.DecimalField(
        verbose_name="Outstanding Balance",
        max_digits=40,
        decimal_places=2,
    )
    FSPBankAccount = models.CharField(
        verbose_name="FSP Bank Account",
        max_length=45,
    )
    FSPBankAccountName = models.CharField(
        verbose_name="FSP Bank Account Name",
        max_length=250,
    )
    SWIFTCode = models.CharField(
        verbose_name="Swift Code",
        max_length=45,
    )
    MNOChannels = models.CharField(
        verbose_name="MNO Channels",
        max_length=45,
    )
    FinalPaymentDate = models.DateTimeField(
        verbose_name="Final Payment Date",
    )
    LastDeductionDate = models.DateTimeField(
        verbose_name="Last Deduction Date",
    )
    LastPayDate = models.DateTimeField(
        verbose_name="Last Payment Date",
    )
    EndDate = models.DateTimeField(
        verbose_name="End Date",
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
        return f'{self.FSPReferenceNumber} : {self.LoanNumber}'

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Loan Takeover Detail"
        verbose_name_plural = "Loan Takeover Detail"
