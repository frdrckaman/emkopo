from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class LoanDeductionRecord(BaseUuidModel):
    LoanNumber = models.CharField(
        verbose_name="Loan Number",
        max_length=20,
    )
    CheckNumber = models.IntegerField(
        verbose_name="Check number",
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
    NationalId = models.CharField(
        verbose_name="National ID",
        max_length=45,
    )
    VoteCode = models.CharField(
        verbose_name="Vote code",
        max_length=6,
    )
    VoteName = models.CharField(
        verbose_name="Vote name",
        max_length=255,
    )
    DepartmentCode = models.CharField(
        verbose_name="Department Code",
        max_length=45,
    )
    DepartmentName = models.CharField(
        verbose_name="Department Name",
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
    BalanceAmount = models.DecimalField(
        verbose_name="Balance Amount",
        max_digits=40,
        decimal_places=2,
    )
    DeductionAmount = models.DecimalField(
        verbose_name="Deduction Amount",
        max_digits=40,
        decimal_places=2,
    )
    HasStopPay = models.BooleanField(
        verbose_name="Has stop pay",
    )
    StopPayReason = models.CharField(
        verbose_name="Stop pay reason",
        max_length=255,
    )
    CheckDate = models.DateField(
        verbose_name="Check date",
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
        verbose_name = "Loan Deduction Record"
        verbose_name_plural = "Loan Deduction Records"
