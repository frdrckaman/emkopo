from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class LoanChargeRequest(BaseUuidModel):
    CheckNumber = models.IntegerField(
        verbose_name="Check number",
    )
    DesignationCode = models.CharField(
        verbose_name="Designation code",
        max_length=8,
    )
    DesignationName = models.CharField(
        verbose_name="Designation name",
        max_length=255,
    )
    BasicSalary = models.DecimalField(
        verbose_name="Basic Salary",
        max_digits=40,
        decimal_places=2,
    )
    NetSalary = models.DecimalField(
        verbose_name="Net salary",
        max_digits=40,
        decimal_places=2,
    )
    OneThirdAmount = models.DecimalField(
        verbose_name="One third amount",
        max_digits=40,
        decimal_places=2,
    )
    RequestedAmount = models.DecimalField(
        verbose_name="Requested amount",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    DeductibleAmount = models.DecimalField(
        verbose_name="Deductible amount",
        max_digits=40,
        decimal_places=2,
    )
    DesiredDeductibleAmount = models.DecimalField(
        verbose_name="Desired deductible amount",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    RetirementDate = models.IntegerField(
        verbose_name="Retirement date",
    )
    TermsOfEmployment = models.CharField(
        verbose_name="Terms of employment",
        max_length=30,
    )
    Tenure = models.IntegerField(
        verbose_name="Tenure",
        blank=True,
        null=True,
    )
    ProductCode = models.CharField(
        verbose_name="Product code",
        max_length=8,
    )
    VoteCode = models.CharField(
        verbose_name="Vote Code",
        max_length=10,
    )
    TotalEmployeeDeduction = models.DecimalField(
        verbose_name="Total Employee Deduction",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    JobClassCode = models.CharField(
        verbose_name="Job class code",
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
        return f'{self.CheckNumber} : {self.DesignationName}'

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Loan Charge Request"
        verbose_name_plural = "Loan Charge Requests"
