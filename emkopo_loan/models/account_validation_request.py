from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class AccountValidationRequest(BaseUuidModel):
    AccountNumber = models.CharField(
        verbose_name="Account Number",
        max_length=455,
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
        return f'{self.AccountNumber}'

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Account Validation Request"
        verbose_name_plural = "Account Validation Requests"