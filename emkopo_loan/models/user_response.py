from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import OFFER_RESPONSE, YES_NO
from emkopo_mixins.model import BaseUuidModel
from emkopo_loan.models import LoanOfferRequest


class UserResponse(BaseUuidModel):
    Staff = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_responses",
        verbose_name="Staff"
    )
    LoanOfferRequest = models.ForeignKey(
        LoanOfferRequest,
        on_delete=models.CASCADE,
        related_name="loan_request",
        verbose_name="Loan Offer Request"
    )
    FspComplies = models.CharField(
        verbose_name="Complies to business rules",
        max_length=45,
        choices=YES_NO,
    )
    FspResponse = models.CharField(
        verbose_name="Offer Response",
        max_length=10,
        choices=OFFER_RESPONSE,
        default='0'
    )
    Timestamp = models.DateTimeField(
        verbose_name="Timestamp",
        default=timezone.now
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.LoanOfferRequest

    class Meta(BaseUuidModel.Meta):
        verbose_name = "User Response"
        verbose_name_plural = "User Responses"
