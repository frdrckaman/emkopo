from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from emkopo_constants.choices import REQUEST_TYPE
from emkopo_mixins.model import BaseUuidModel


class ApiRequest(BaseUuidModel):
    MessageType = models.CharField(
        verbose_name="Message Type",
        max_length=100,
    )
    RequestType = models.CharField(
        verbose_name="System Name",
        max_length=45,
        choices=REQUEST_TYPE,
    )
    TimeStamp = models.DateTimeField(
        verbose_name="Timestamp",
        default=timezone.now,
    )
    ApiUrl = models.CharField(
        verbose_name="ApiUrl",
        max_length=255,
    )
    PayLoad = models.TextField(
        verbose_name="PayLoad",
    )
    Signature = models.TextField(
        verbose_name="Signature",
    )
    Status = models.IntegerField(
        verbose_name="Status",
        default=200,
    )

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.MessageType}: {self.RequestType}"

    class Meta(BaseUuidModel.Meta):
        verbose_name = "API Request"
        verbose_name_plural = "API Requests"
