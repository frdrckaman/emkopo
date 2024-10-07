from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class LoanLiquidationRequest(BaseUuidModel):
    ProductCode = models.IntegerField(
        verbose_name="Product Code",
    )
    LoanAmount = models.DecimalField(
        verbose_name="Loan Amount",
        max_digits=40,
        decimal_places=2,
    )
    DeductionAmount = models.DecimalField(
        verbose_name="Deduction Amount",
        max_digits=40,
        decimal_places=2,
    )
    TakeOverBalance = models.DecimalField(
        verbose_name="Take Over Balance",
        max_digits=40,
        decimal_places=2,
    )
    FSP1Code = models.CharField(
        verbose_name="FSP1 Code",
        max_length=45,
    )
    FSP1Name = models.CharField(
        verbose_name="FSP1 Name",
        max_length=120,
    )
    FSP1LoanNumber = models.CharField(
        verbose_name="FSP1 Loan Number",
        max_length=45,
    )
    FSP1PaymentReferenceNumber = models.CharField(
        verbose_name="FSP1 Payment Reference Number",
        max_length=45,
    )
    NetLoanAmount = models.DecimalField(
        verbose_name="NetLoan Amount",
        max_digits=40,
        decimal_places=2,
    )
    TotalAmountToPay = models.DecimalField(
        verbose_name="Total Amount To Pay",
        max_digits=40,
        decimal_places=2,
    )
    PaymentRate = models.CharField(
        verbose_name="Payment Rate",
        max_length=50,
    )
    Reserved3 = models.CharField(
        verbose_name="Reserved3",
        max_length=6,
    )
    TermsAndConditionsNumber = models.CharField(
        verbose_name="Terms And Conditions Number",
        max_length=45,
    )
    ApplicationNumber = models.CharField(
        verbose_name="Application Number",
        max_length=45,
    )
    FSPReferenceNumber = models.CharField(
        verbose_name="FSPReference Number",
        max_length=45,
    )
    ApproverName = models.CharField(
        verbose_name="Approver Name",
        max_length=45,
    )
    ApproverDesignation = models.CharField(
        verbose_name="Approver Designation",
        max_length=60,
    )
    ApproverWorkstation = models.CharField(
        verbose_name="Approver Workstation",
        max_length=45,
        blank=True,
        null=True,
    )
    ApproverInstitution = models.CharField(
        verbose_name="Approver Institution",
        max_length=255,
    )
    ActionDateAndTime = models.DateTimeField(
        verbose_name="Action Date And Time",
    )
    ContactPerson = models.CharField(
        verbose_name="Contact Person",
        max_length=90,
        blank=True,
        null=True,
    )
    ApprovalReferenceNumber = models.CharField(
        verbose_name="Approval Reference Number",
        max_length=45,
        blank=True,
        null=True,
    )
    Status = models.CharField(
        verbose_name="Status",
        max_length=30,
    )
    Reason = models.TextField(
        verbose_name="Reason",
        blank=True,
        null=True,
    )
    Comments = models.TextField(
        verbose_name="Comments",
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

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.FSP1LoanNumber} : {self.ApplicationNumber}'

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Loan Liquidation Request"
        verbose_name_plural = "Loan Liquidation Requests"
