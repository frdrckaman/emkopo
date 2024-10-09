from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class LoanLiquidationNotification(BaseUuidModel):
    PaymentReference = models.CharField(
        verbose_name="Payment Reference",
        max_length=45,
    )
    ApplicationNumber = models.CharField(
        verbose_name="Application Number",
        max_length=45,
    )
    ApproverName = models.CharField(
        verbose_name="Approver Name",
        max_length=120,
    )
    ApproverDesignation = models.CharField(
        verbose_name="Approver Designation",
        max_length=45,
    )
    ApproverWorkstation = models.CharField(
        verbose_name="Approver Workstation",
        max_length=255,
    )
    ApproverInstitution = models.CharField(
        verbose_name="Approver Institution",
        max_length=45,
    )
    ActionDateAndTime = models.DateTimeField(
        verbose_name="Action Date And Time",
    )
    ContactPerson = models.CharField(
        verbose_name="Contact Person",
        max_length=45,
    )
    MonthlyPrincipal = models.DecimalField(
        verbose_name="Monthly Principal",
        max_digits=40,
        decimal_places=2,
    )
    MonthlyInterest = models.DecimalField(
        verbose_name="Monthly Interest",
        max_digits=4,
        decimal_places=2,
    )
    MonthlyInstalment = models.DecimalField(
        verbose_name="Monthly Instalment",
        max_digits=40,
        decimal_places=2,
    )
    OutstandingBalance = models.DecimalField(
        verbose_name="Outstanding Balance",
        max_digits=40,
        decimal_places=2,
    )
    DeductionStartDate = models.DateTimeField(
        verbose_name="Deduction Start Date",
    )
    DeductionEndDate = models.DateTimeField(
        verbose_name="Deduction End Date",
    )
    FSPReferenceNumber = models.CharField(
        verbose_name="FSPReferenceNumber",
        max_length=45,
    )
    CheckNumber = models.CharField(
        verbose_name="CheckNumber",
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
        verbose_name = "Loan Liquidation Notification"
        verbose_name_plural = "Loan Liquidation Notification"
