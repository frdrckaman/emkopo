from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class LoanDefaulterDetail(BaseUuidModel):
    CheckNumber = models.CharField(
        verbose_name="CheckNumber",
        max_length=45,
    )
    LoanNumber = models.CharField(
        verbose_name="Loan Number",
        max_length=45,
    )
    FSPCode = models.CharField(
        verbose_name="FSPCode",
        max_length=45,
    )
    LastPaymentDate = models.DateField(
        verbose_name="Last Payment Date",
    )
    EmploymentStatus = models.CharField(
        verbose_name="Employment Status",
        max_length=45,
        blank=True,
        null=True,
    )
    PhysicalAddress = models.CharField(
        verbose_name="Physical Address",
        max_length=255,
        blank=True,
        null=True,
    )
    TelephoneNumber = models.CharField(
        verbose_name="Telephone Number",
        max_length=45,
        blank=True,
        null=True,
    )
    EmailAddress = models.CharField(
        verbose_name="Email Address",
        max_length=45,
    )
    Fax = models.CharField(
        verbose_name="Fax",
        max_length=45,
    )
    MobileNumber = models.CharField(
        verbose_name="Mobile Number",
        max_length=45,
    )
    ContactPerson = models.CharField(
        verbose_name="Contact Person",
        max_length=120,
    )
    Institution = models.CharField(
        verbose_name="Institution",
        max_length=255,
        blank=True,
        null=True,
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
        verbose_name = "Loan Defaulter Detail"
        verbose_name_plural = "Loan Defaulter Detail"
