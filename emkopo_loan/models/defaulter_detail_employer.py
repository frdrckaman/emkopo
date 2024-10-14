from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class LoanDefaulterDetailEmployer(BaseUuidModel):
    CheckNumber = models.CharField(
        verbose_name="CheckNumber",
        max_length=45,
    )
    LoanNumber = models.CharField(
        verbose_name="Loan Number",
        max_length=45,
    )
    VoteName = models.CharField(
        verbose_name="Vote Name",
        max_length=255,
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
    InstallationAmount = models.DecimalField(
        verbose_name="Installation Amount",
        decimal_places=2,
        max_digits=40,
    )
    DeductionAmount = models.DecimalField(
        verbose_name="Deduction Amount",
        decimal_places=2,
        max_digits=40,
    )
    DeductionCode = models.CharField(
        verbose_name="Deduction Code",
        max_length=45,
    )
    DeductionName = models.CharField(
        verbose_name="Deduction Name",
        max_length=45,
    )
    OutstandingBalance = models.DecimalField(
        verbose_name="Outstanding Balance",
        decimal_places=2,
        max_digits=40,
    )
    LastPayDate = models.DateField(
        verbose_name="Last Payment Date",
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
        verbose_name = "Loan Defaulter Detail Employer"
        verbose_name_plural = "Loan Defaulter Detail Employer"
