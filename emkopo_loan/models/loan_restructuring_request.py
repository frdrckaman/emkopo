from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class LoanRestructuringRequest(BaseUuidModel):
    ApplicationNumber = models.CharField(
        verbose_name="Application Number",
        max_length=45,
    )
    LoanNumber = models.CharField(
        verbose_name="Loan Number",
        max_length=20,
    )
    Comments = models.CharField(
        verbose_name="Comments",
        max_length=255,
    )
    LoanOutstandingAmount = models.DecimalField(
        verbose_name="Loan Outstanding Amount",
        max_digits=40,
        decimal_places=2,
    )
    NewLoanAmount = models.DecimalField(
        verbose_name="New Loan Amount",
        max_digits=40,
        decimal_places=2,
    )
    NewInstallmentAmount = models.DecimalField(
        verbose_name="New Installment Amount",
        max_digits=40,
        decimal_places=2,
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
        return f'{self.ApplicationNumber} : {self.LoanNumber}'

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Loan Restructuring Request"
        verbose_name_plural = "Loan Restructuring Requests"
