from django.db import models
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel
from emkopo_loan.models import LoanChargeRequest


class LoanChargeResponse(BaseUuidModel):
    LoanChargeRequest = models.ForeignKey(
        LoanChargeRequest,
        on_delete=models.CASCADE,
        related_name='loan_charge_responses',
        verbose_name='Loan Charge Request'
    )
    DesiredDeductibleAmount = models.DecimalField(
        verbose_name="Desired deductible amount",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    TotalInsurance = models.DecimalField(
        verbose_name="Total Insurance",
        max_digits=40,
        decimal_places=2,
    )
    TotalProcessingFees = models.DecimalField(
        verbose_name="Total Processing Fees",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    TotalInterestRateAmount = models.DecimalField(
        verbose_name="Total Interest Rate Amount",
        max_digits=40,
        decimal_places=2,
    )
    OtherCharges = models.DecimalField(
        verbose_name="Other Charges",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    NetLoanAmount = models.DecimalField(
        verbose_name="Net Loan Amount",
        max_digits=40,
        decimal_places=2,
    )
    TotalAmountToPay = models.DecimalField(
        verbose_name="Total Amount To Pay",
        max_digits=40,
        decimal_places=2,
    )
    Tenure = models.IntegerField(
        verbose_name="Tenure",
    )
    EligibleAmount = models.DecimalField(
        verbose_name="Eligible Amount",
        max_digits=40,
        decimal_places=2,
        blank=True,
        null=True,
    )
    MonthlyReturnAmount = models.DecimalField(
        verbose_name="Monthly Return Amount",
        max_digits=40,
        decimal_places=2,
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
    status = models.IntegerField(
        verbose_name="Status",
        default=1,
    )

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.LoanChargeRequest}'

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Loan Charge Response"
        verbose_name_plural = "Loan Charge Responses"
