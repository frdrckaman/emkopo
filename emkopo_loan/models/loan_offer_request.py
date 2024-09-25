from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE, LOAN_TYPE
from emkopo_constants.constants import NEW_LOAN
from emkopo_mixins.model import BaseUuidModel


class LoanOfferRequest(BaseUuidModel):
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
    Sex = models.CharField(
        verbose_name="Sex",
        max_length=1,
        blank=True,
        null=True,
    )
    BankAccountNumber = models.CharField(
        verbose_name="Bank Account Number",
        max_length=20,
        blank=True,
        null=True,
    )
    EmploymentDate = models.CharField(
        verbose_name="Employment Date",
        max_length=10,
        blank=True,
        null=True,
    )
    MaritalStatus = models.CharField(
        verbose_name="Marital Status",
        max_length=10,
        blank=True,
        null=True,
    )
    ConfirmationDate = models.CharField(
        verbose_name="Confirmation Date",
        max_length=10,
        blank=True,
        null=True,
    )
    TotalEmployeeDeduction = models.DecimalField(
        verbose_name="Total Employee Deduction",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    NearestBranchName = models.CharField(
        verbose_name="Nearest Branch Name",
        max_length=50,
        blank=True,
        null=True,
    )
    VoteCode = models.CharField(
        verbose_name="Vote code",
        max_length=6,
    )
    VoteName = models.CharField(
        verbose_name="Vote name",
        max_length=255,
    )
    NIN = models.CharField(
        verbose_name="NIN",
        max_length=22,
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
        verbose_name="One Third Amount",
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
    DesiredDeductibleAmount = models.DecimalField(
        verbose_name="Desired deductible amount",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    RetirementDate = models.CharField(
        verbose_name="Retirement date",
        max_length=12,
        blank=True,
        null=True,
    )
    TermsOfEmployment = models.CharField(
        verbose_name="Terms of employment",
        max_length=30,
    )
    Tenure = models.IntegerField(
        verbose_name="Tenure",
    )
    ProductCode = models.CharField(
        verbose_name="Product code",
        max_length=8,
    )
    InterestRate = models.DecimalField(
        verbose_name="Interest rate",
        max_digits=40,
        decimal_places=2,
    )
    ProcessingFee = models.DecimalField(
        verbose_name="Processing fee",
        max_digits=40,
        decimal_places=2,
    )
    Insurance = models.DecimalField(
        verbose_name="Insurance",
        max_digits=40,
        decimal_places=2,
    )
    PhysicalAddress = models.CharField(
        verbose_name="Physical address",
        max_length=50,
        blank=True,
        null=True,
    )
    TelephoneNumber = models.CharField(
        verbose_name="Telephone number",
        max_length=12,
        blank=True,
        null=True,
    )
    EmailAddress = models.CharField(
        verbose_name="Email address",
        max_length=50,
        blank=True,
        null=True,
    )
    MobileNumber = models.CharField(
        verbose_name="Mobile number",
        max_length=12,
        blank=True,
        null=True,
    )
    ApplicationNumber = models.CharField(
        verbose_name="Application number",
        max_length=12,
    )
    LoanPurpose = models.CharField(
        verbose_name="Loan Purpose",
        max_length=250,
        blank=True,
        null=True,
    )
    ContractStartDate = models.CharField(
        verbose_name="Contract Start Date",
        max_length=10,
        blank=True,
        null=True,
    )
    ContractEndDate = models.CharField(
        verbose_name="Contract End Date",
        max_length=10,
        blank=True,
        null=True,
    )
    LoanNumber = models.CharField(
        verbose_name="Loan Number",
        max_length=20,
        blank=True,
        null=True,
    )
    FSPReferenceNumber = models.CharField(
        verbose_name="FSP Reference Number",
        max_length=45,
        blank=True,
        null=True,
    )
    SettlementAmount = models.DecimalField(
        verbose_name="Settlement amount",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    LoanOfferType = models.CharField(
        verbose_name="Loan Offer Type",
        max_length=45,
        choices=LOAN_TYPE,
        default=NEW_LOAN,
    )
    TotalAmountToPay = models.DecimalField(
        verbose_name="Total Amount to Pay",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    DisbursementDate = models.DateTimeField(
        verbose_name="Disbursement date",
        blank=True,
        null=True,
    )
    PaymentReferenceNumber = models.CharField(
        verbose_name="Payment Reference Number",
        max_length=45,
        blank=True,
        null=True,
    )
    FSP1Code = models.CharField(
        verbose_name="FSP1 Code",
        max_length=8,
        blank=True,
        null=True,
    )
    FSP1LoanNumber = models.CharField(
        verbose_name="FSP1 Loan Number",
        max_length=8,
        blank=True,
        null=True,
    )
    TakeOverBalance = models.DecimalField(
        verbose_name="Take over balance",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    FSP1EndDate = models.DateTimeField(
        verbose_name="FSP1 End Date",
        blank=True,
        null=True,
    )
    FSP1LastDeductionDate = models.DateTimeField(
        verbose_name="FSP1 Last Deduction",
        blank=True,
        null=True,
    )
    FSP1BankAccount = models.CharField(
        verbose_name="FSP1 Bank Account",
        max_length=20,
        blank=True,
        null=True,
    )
    FSP1BankAccountName = models.CharField(
        verbose_name="FSP1 Bank Account Name",
        max_length=100,
        blank=True,
        null=True,
    )
    FSP1SWIFTCode = models.CharField(
        verbose_name="FSP1 SWIFT Code",
        max_length=20,
        blank=True,
        null=True,
    )
    FSP1MNOChannels = models.CharField(
        verbose_name="FSP1 MNO Channels",
        max_length=20,
        blank=True,
        null=True,
    )
    FSP1PaymentReferenceNumber = models.CharField(
        verbose_name="FSP1 Payment Reference Number",
        max_length=10,
        blank=True,
        null=True,
    )
    FSP1FinalPaymentDate = models.DateTimeField(
        verbose_name="FSP1 Final Payment Date",
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
    Reason = models.CharField(
        verbose_name="Reason",
        max_length=255,
        blank=True,
        null=True,
    )
    FailureReason = models.CharField(
        verbose_name="Disbursement Failure Reason",
        max_length=255,
        blank=True,
        null=True,
    )
    CancellationReason = models.CharField(
        verbose_name="Offer Cancellation Reason Reason",
        max_length=255,
        blank=True,
        null=True,
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
        return f'{self.CheckNumber} : {self.ApplicationNumber}'

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Loan Offer Request"
        verbose_name_plural = "Loan Offer Requests"
